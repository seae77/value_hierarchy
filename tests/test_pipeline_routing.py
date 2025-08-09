import types
import builtins

import pytest

from domain.hypothesis_types import HypothesisType
from domain.values import Value, ValuePair
from master_psy import pipeline as pl


class DummyOpenAIClient:
    def __init__(self):
        self.model_scenario = "test-scenario"
        self.model_vignette = "test-vignette"
        self.model_question = "test-question"

    def _generate_content(self, system_prompt, user_prompt, model, temperature, max_tokens):
        return f"CONTENT[{model}]"

    def generate_scenario(self, prompt, temperature=0.5, max_tokens=300):
        return "SCENARIO"

    def generate_vignette(self, prompt, temperature=0.0, max_tokens=300):
        return "VIGNETTE"

    def generate_question(self, prompt, temperature=0.0, max_tokens=100):
        return "QUESTION"


@pytest.fixture
def dummy_pair():
    v1 = Value(name="A", definition="defA", descriptive_keywords=["ka"], example_phrases=["pa"])
    v2 = Value(name="B", definition="defB", descriptive_keywords=["kb"], example_phrases=["pb"])
    return ValuePair(v1, v2)


def test_pipeline_routing_handles_hypotheses(monkeypatch, dummy_pair):
    # Intercept generate_value_pair to only yield one pair to keep test fast
    monkeypatch.setattr(pl, "generate_value_pair", lambda: [dummy_pair])

    # Inject dummy OpenAI client and reviewer methods
    dummy_client = DummyOpenAIClient()

    # Monkeypatch OpenAIClient constructor to return our dummy client
    monkeypatch.setattr(pl, "OpenAIClient", lambda api_key, model_scenario, model_vignette, model_question: dummy_client)

    # Ensure env api key exists for the test
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    # Capture outputs by monkeypatching save_to_pdf to assert structure
    recorded = {}

    def fake_save_to_pdf(value_pair, results, output_dir="output"):
        recorded["pair"] = value_pair
        recorded["results"] = results
        recorded["output_dir"] = output_dir

    monkeypatch.setattr(pl, "save_to_pdf", fake_save_to_pdf)

    # Run the main pipeline
    pl.main()

    # We expect H4 to be skipped; H1, H2, H3, H5, H6 to be present
    hyp_set = {r["hypothesis"] for r in recorded["results"]}
    assert "H4" not in hyp_set
    for h in ["H1", "H2", "H3", "H5", "H6"]:
        assert h in hyp_set

    # Check H2 stored two questions
    h2_entry = next(r for r in recorded["results"] if r["hypothesis"] == "H2")
    assert "questions" in h2_entry and set(h2_entry["questions"].keys()) == {"H2", "H5"}


def test_pdf_output_dir_defaults(monkeypatch, dummy_pair):
    monkeypatch.setattr(pl, "generate_value_pair", lambda: [dummy_pair])
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    dummy_client = DummyOpenAIClient()
    monkeypatch.setattr(pl, "OpenAIClient", lambda api_key, model_scenario, model_vignette, model_question: dummy_client)

    captured = {}

    def fake_save_to_pdf(value_pair, results, output_dir="output"):
        captured["output_dir"] = output_dir

    monkeypatch.setattr(pl, "save_to_pdf", fake_save_to_pdf)

    # Unset OUTPUT_DIR to use default
    monkeypatch.delenv("OUTPUT_DIR", raising=False)
    pl.main()

    assert captured["output_dir"] == "output"

