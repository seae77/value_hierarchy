import logging
import os
from pathlib import Path
import time
from generator.vignette_reviewer import VignetteReviewer
from domain.hypothesis_types import HypothesisType
from domain.values import generate_value_pair
from generator.vignette_generator import (
    generate_single_scenario_prompt,
    combine_scenarios_prompt
)
from generator.vignette_generator import (
    generate_question_prompt_h1,
    generate_question_prompt_h2,
    generate_question_prompt_h3,
    generate_question_prompt_h4,
    generate_question_prompt_h5,
    generate_question_prompt_h6
)
from output.pdf_saver import save_to_pdf
from utils.logging_utils import setup_logging
from generator.openai_client import OpenAIClient


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set. Please set it or create a .env file.")
        return

    output_dir = os.getenv("OUTPUT_DIR", "output")

    num_pairs = 15  # for demo
    openai_client = OpenAIClient(
        api_key=api_key,
        model_scenario="gpt-4o",
        model_vignette="gpt-4o",
        model_question="gpt-4o"
    )
    reviewer = VignetteReviewer(openai_client)

    value_pairs = generate_value_pair()
    for pair in value_pairs:
        logger.info(f"=== Processing ValuePair: {pair.value1.name} vs {pair.value2.name} ===")

        # 1) Create scenario prompts
        scenarioA_prompt = generate_single_scenario_prompt(pair.value1)
        scenarioB_prompt = generate_single_scenario_prompt(pair.value2)

        # 2) Get final scenario text from OpenAI
        scenarioA = openai_client.generate_scenario(scenarioA_prompt)
        scenarioB = openai_client.generate_scenario(scenarioB_prompt)

        logger.debug(f"scenarioA ({pair.value1.name}):\n{scenarioA}")
        logger.debug(f"scenarioB ({pair.value2.name}):\n{scenarioB}")

        if not scenarioA or not scenarioB:
            logger.error("Could not generate valid single scenarios for the pair, skipping.")
            continue

        pair_results = []

        # Define pipeline mapping to reduce duplication
        PIPELINE = {
            HypothesisType.H1: {
                "reviewer": reviewer.review_vignette_h1,
                "prompts": [("question", generate_question_prompt_h1)],
            },
            HypothesisType.H2: {
                "reviewer": reviewer.review_vignette_h2,
                # Generate both H2 and H5 questions from the same reviewed vignette
                "prompts": [("H2", generate_question_prompt_h2), ("H5", generate_question_prompt_h5)],
            },
            HypothesisType.H3: {
                "reviewer": reviewer.review_vignette_h3,
                "prompts": [("question", generate_question_prompt_h3)],
            },
            HypothesisType.H5: {
                "reviewer": reviewer.review_vignette_h5,
                "prompts": [("question", generate_question_prompt_h5)],
            },
            HypothesisType.H6: {
                "reviewer": reviewer.review_vignette_h6,
                "prompts": [("question", generate_question_prompt_h6)],
            },
        }

        # 3) For each hypothesis, combine into a final vignette, then generate question(s)
        for hypothesis in HypothesisType:
            # Skip HypothesisType.H4
            if hypothesis == HypothesisType.H4:
                continue

            # a) Build the combination prompt from the two scenario texts
            combined_vignette_prompt = combine_scenarios_prompt(scenarioA, scenarioB, hypothesis, pair)
            logger.debug(f"combined_vignette_prompt ({hypothesis.value}):\n{combined_vignette_prompt}")

            if not combined_vignette_prompt:
                logger.error(f"Error building combined prompt for {hypothesis.value}")
                continue

            # b) Get the final combined vignette text from OpenAI
            combined_vignette = openai_client.generate_vignette(combined_vignette_prompt)
            if not combined_vignette:
                logger.error(f"Error generating combined vignette for {hypothesis.value}")
                continue

            # c) Review the vignette according to the hypothesis
            reviewer_fn = PIPELINE[hypothesis]["reviewer"]
            reviewed_vignette = reviewer_fn(combined_vignette, pair)
            logger.debug(
                f"reviewed_vignette ({hypothesis.value}, {pair.value1.name} vs {pair.value2.name}):\n{reviewed_vignette}"
            )

            # d) Generate question prompt(s) and question(s)
            prompt_entries = PIPELINE[hypothesis]["prompts"]

            if len(prompt_entries) == 1:
                label, prompt_fn = prompt_entries[0]
                question_prompt = prompt_fn(reviewed_vignette, pair)
                logger.debug(f"question_prompt ({hypothesis.value}):\n{question_prompt}")

                question = openai_client.generate_question(question_prompt)
                if not question:
                    logger.error(f"Error generating question for {hypothesis.value}")
                    continue
                logger.debug(
                    f"question ({hypothesis.value}, {pair.value1.name} vs {pair.value2.name}):\n{question}"
                )

                pair_results.append({
                    "hypothesis": hypothesis.value,
                    "vignette": combined_vignette,
                    "question": question,
                })
            else:
                questions = {}
                for label, prompt_fn in prompt_entries:
                    q_prompt = prompt_fn(reviewed_vignette, pair)
                    logger.debug(f"question_prompt {label} ({hypothesis.value}):\n{q_prompt}")

                    q = openai_client.generate_question(q_prompt)
                    if not q:
                        logger.error(f"Error generating {label} question for {hypothesis.value}")
                        continue
                    questions[label] = q

                # Ensure all expected questions were generated
                if len(questions) != len(prompt_entries):
                    logger.error(f"Error generating all questions for {hypothesis.value}")
                    continue

                pair_results.append({
                    "hypothesis": hypothesis.value,
                    "vignette": combined_vignette,
                    "questions": questions,
                })

        # 4) Save results
        if pair_results:
            try:
                save_to_pdf(pair, pair_results, output_dir=output_dir)
            except Exception as e:
                logger.error(f"Failed to save PDF: {str(e)}")


if __name__ == "__main__":
    from master_psy.pipeline import main as pipeline_main
    pipeline_main()
