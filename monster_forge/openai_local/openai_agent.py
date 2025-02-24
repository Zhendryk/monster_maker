import requests
import os
from pathlib import Path
from openai import OpenAI
from monster_forge.openai_local.constants import (
    OPENAPI_SECRET_KEY,
    ORGANIZATION_ID,
    PROJECT_ID,
)
from monster_forge.openai_local.enums import (
    OpenAIModel,
    DallEImageSize,
    DallEImageQuality,
)


class OpenAIAgent:
    def __init__(
        self,
        api_key: str = OPENAPI_SECRET_KEY,
        organization_id: str = ORGANIZATION_ID,
        project_id: str = PROJECT_ID,
    ) -> None:
        self._client = OpenAI(
            api_key=api_key, organization=organization_id, project=project_id
        )

    def generate_text(
        self,
        prompt: str,
        model: OpenAIModel = OpenAIModel.MODEL_4O_MINI,
        store: bool = False,
        max_completion_tokens: int = 2048,
    ) -> str | None:
        completion = self._client.chat.completions.create(
            model=model.api_name,
            store=store,
            max_completion_tokens=max_completion_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content

    def generate_image(
        self,
        prompt: str,
        model: OpenAIModel = OpenAIModel.MODEL_DALL_E_3,
        size: DallEImageSize = DallEImageSize.SIZE_1024_X_1024,
        quality: DallEImageQuality = DallEImageQuality.HD,
        allow_prompt_rewriting: bool = True,
        num_images: int = 1,
        download_image_to_file: bool = False,
        download_filepath: Path | None = None,
    ) -> tuple[str | None, str | None]:
        if not model.is_image_model:
            raise ValueError(f"Invalid model for image generation: {model.api_name}")
        if num_images > model.num_images_supported:
            raise ValueError(
                f"Invalid number of images to generate ({num_images}). {model.api_name} only supports up to {model.num_images_supported}."
            )
        if not model.supports_image_size(size):
            raise ValueError(
                f"Model {model.api_name} does not support image size: {size.api_name}"
            )
        if not model.supports_image_quality(quality):
            raise ValueError(
                f"Model {model.api_name} does not support image quality: {quality.api_name}"
            )
        if download_image_to_file and download_filepath is None:
            raise ValueError(
                "Requested to download image but no filepath to save it to was provided."
            )
        if not allow_prompt_rewriting:
            prompt = f"{prompt}. I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS."
        if not download_filepath.parent.exists():
            os.makedirs(download_filepath.parent, exist_ok=True)
        response = self._client.images.generate(
            model=model.api_name,
            prompt=prompt,
            size=size.api_name,
            quality=quality.api_name,
            n=num_images,
        )
        revised_prompt = response.data[0].revised_prompt
        generated_image_url = response.data[0].url
        if download_image_to_file:
            img_data = requests.get(generated_image_url).content
            with open(download_filepath, "wb") as image_file:
                image_file.write(img_data)
            print(f"Generated image downloaded to: {download_filepath.resolve()}")
        return revised_prompt, generated_image_url
