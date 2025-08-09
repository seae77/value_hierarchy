import logging
from typing import Optional
from openai import OpenAI


class OpenAIClient:
    """Thin wrapper around the OpenAI SDK used by this project.

    Provides convenience methods to generate scenarios, vignettes, and questions
    with consistent defaults.
    """

    def __init__(
        self,
        api_key: str,
        model_scenario: str = "gpt-4",
        model_vignette: str = "gpt-4",
        model_question: str = "gpt-4",
    ) -> None:
        """Initialize the client with explicit models.

        Args:
            api_key: OpenAI API key used to authenticate requests.
            model_scenario: Model name to use for scenario generation.
            model_vignette: Model name to use for vignette generation.
            model_question: Model name to use for question generation.
        """
        self.client = OpenAI(api_key=api_key)
        self.model_scenario = model_scenario
        self.model_vignette = model_vignette
        self.model_question = model_question
        self.logger = logging.getLogger(self.__class__.__name__)

    def _generate_content(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 300,
    ) -> str:
        """Base method for generating content using Chat Completions.

        Returns an empty string on error and logs the exception.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content.strip()
            self.logger.debug(f"Generated content:\n{content}")
            return content
        except Exception as e:
            self.logger.error(f"OpenAI error: {e}")
            return ""

    def generate_scenario(
        self,
        prompt: str,
        temperature: float = 0.5,
        max_tokens: int = 300,
    ) -> str:
        """Generate a single scenario text from a user-provided prompt."""
        system_prompt = (
            "Vous êtes ChatGPT. Vous allez produire exactement le texte du scénario tel qu'il vous a été demandé, "
            "en restant neutre et factuel."
        )
        return self._generate_content(
            system_prompt=system_prompt,
            user_prompt=prompt,
            model=self.model_scenario,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def generate_vignette(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 300,
    ) -> str:
        """Generate the final combined vignette text from a user-provided prompt."""
        system_prompt = (
            "Vous êtes ChatGPT. Vous allez produire exactement le texte de la vignette tel qu'il vous a été demandé, "
            "en restant neutre et factuel."
        )
        return self._generate_content(
            system_prompt=system_prompt,
            user_prompt=prompt,
            model=self.model_vignette,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def generate_question(
        self,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 100,
    ) -> str:
        """Generate the final question text from a user-provided question prompt."""
        system_prompt = (
            "Vous êtes ChatGPT. Vous allez produire exactement le texte de la question tel qu'il vous a été demandé, "
            "en restant neutre et factuel."
        )
        return self._generate_content(
            system_prompt=system_prompt,
            user_prompt=prompt,
            model=self.model_question,
            temperature=temperature,
            max_tokens=max_tokens,
        )
