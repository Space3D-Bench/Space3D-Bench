from abc import ABC, abstractmethod

from pathlib import Path


class AbstractVisionLLM(ABC):
    """
    Abstract class for LLMs with vision capabilities.
    """

    @abstractmethod
    def get_response(self, prompt: str, system_prompt: str, image_path: Path) -> str:
        """
        Get response from the model given a prompt, system prompt and a path to the
        relevant image.
        """
        raise NotImplementedError


class AbstractTextLLM(ABC):
    """
    Abstract class for text-used-only LLMs.
    """

    @abstractmethod
    def get_response(self, prompt: str, system_prompt: str) -> str:
        """
        Get response from the model given a prompt and a system prompt.
        """
        raise NotImplementedError
