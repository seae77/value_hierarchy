from domain.values import Value, ValuePair
from generator.vignette_generator import (
    generate_single_scenario_prompt,
    combine_scenarios_prompt,
)
from domain.hypothesis_types import HypothesisType


def sample_pair():
    v1 = Value(name="Care", definition="defA", descriptive_keywords=["a"], example_phrases=["p"])
    v2 = Value(name="Fairness", definition="defB", descriptive_keywords=["b"], example_phrases=["p"])
    return ValuePair(v1, v2)


def test_single_scenario_prompt_contains_definition_and_keywords():
    v = Value(name="Care", definition="defA", descriptive_keywords=["a", "b"], example_phrases=["p"])
    prompt = generate_single_scenario_prompt(v)
    assert "EXACTEMENT 60 mots" in prompt or "EXACTEMENT 60" in prompt
    assert "defA" in prompt
    assert "a" in prompt and "b" in prompt


def test_combine_scenarios_varies_by_hypothesis():
    A, B = "Scenario A text", "Scenario B text"
    pair = sample_pair()
    p1 = combine_scenarios_prompt(A, B, HypothesisType.H1, pair)
    p2 = combine_scenarios_prompt(A, B, HypothesisType.H2, pair)
    assert p1 != p2
    assert "EXACTEMENT 110 mots" in p1 or "EXACTEMENT 110" in p1

