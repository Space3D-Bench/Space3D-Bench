from pathlib import Path
from typing import Callable
from io import BytesIO
import base64

from PIL import Image
from openai import AzureOpenAI
from openai.types.chat.chat_completion import ChatCompletion
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from core.abstract_llm import AbstractVisionLLM, AbstractTextLLM



def image_to_data_url(image_path: Path, img_format: str = "PNG") -> str:
    """
    Convert an image (given by its path) to a data URL.
    """
    image: Image.Image = Image.open(image_path)
    image_bytes: BytesIO = BytesIO()
    image.save(image_bytes, format=img_format)
    image_bytes_value: bytes = image_bytes.getvalue()
    base64_encoded_data: str = base64.b64encode(image_bytes_value).decode("utf-8")
    return f"data:image/{img_format.lower()};base64,{base64_encoded_data}"


class ExampleAzureIdentityLLM:
    """
    Example implementation of an LLM-related class that uses Azure Identity for
    authentication.
    """

    def __init__(
        self, endpoint: str, api_version: str, deployment: str, max_tokens: int = 4000
    ) -> None:
        """
        Initialize the Azure OpenAI client with the given endpoint and API version,
        store the deployment and maximum tokens allowed.
        """
        token_provider: Callable[[], str] = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )
        self.deployment: str = deployment
        self.max_tokens: int = max_tokens
        self.client: AzureOpenAI = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version,
        )


class ExampleTextLLM(ExampleAzureIdentityLLM, AbstractTextLLM):
    def get_response(self, prompt: str, system_prompt: str) -> str:
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content


class ExampleVisionLLM(ExampleAzureIdentityLLM, AbstractVisionLLM):
    def get_response(self, prompt: str, system_prompt: str, image_path: Path) -> str:
        data_url: str = image_to_data_url(image_path)
        response: ChatCompletion = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                },
            ],
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
