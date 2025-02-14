from __future__ import annotations
from enum import Enum, auto


class OpenAIModel(Enum):
    MODEL_4O_MINI = auto()
    MODEL_4O = auto()
    MODEL_O1 = auto()
    MODEL_O1_MINI = auto()
    MODEL_O3_MINI = auto()
    MODEL_DALL_E_2 = auto()
    MODEL_DALL_E_3 = auto()

    @property
    def api_name(self) -> str:
        match self:
            case OpenAIModel.MODEL_4O:
                return "gpt-4o"
            case OpenAIModel.MODEL_4O_MINI:
                return "gpt-4o-mini"
            case OpenAIModel.MODEL_O1:
                return "o1"
            case OpenAIModel.MODEL_O1_MINI:
                return "o1-mini"
            case OpenAIModel.MODEL_O3_MINI:
                return "o3-mini"
            case OpenAIModel.MODEL_DALL_E_2:
                return "dall-e-2"
            case OpenAIModel.MODEL_DALL_E_3:
                return "dall-e-3"
            case _:
                raise NotImplementedError

    @property
    def is_reasoning_model(self) -> bool:
        match self:
            case OpenAIModel.MODEL_O1 | OpenAIModel.MODEL_O3_MINI:
                return True
            case _:
                return False

    @property
    def is_image_model(self) -> bool:
        match self:
            case OpenAIModel.MODEL_DALL_E_2 | OpenAIModel.MODEL_DALL_E_3:
                return True
            case _:
                return False

    @property
    def num_images_supported(self) -> int:
        match self:
            case OpenAIModel.MODEL_DALL_E_2:
                return 10
            case OpenAIModel.MODEL_DALL_E_3:
                return 1
            case _:
                raise NotImplementedError

    def supports_image_size(self, size: DallEImageSize) -> bool:
        match self:
            case OpenAIModel.MODEL_DALL_E_2:
                return size in [
                    DallEImageSize.SIZE_256_X_256,
                    DallEImageSize.SIZE_512_X_512,
                    DallEImageSize.SIZE_1024_X_1024,
                ]
            case OpenAIModel.MODEL_DALL_E_3:
                return size in [
                    DallEImageSize.SIZE_1024_X_1024,
                    DallEImageSize.SIZE_1024_X_1792,
                    DallEImageSize.SIZE_1792_X_1024,
                ]
            case _:
                return False

    def supports_image_quality(self, quality: DallEImageQuality) -> bool:
        match self:
            case OpenAIModel.MODEL_DALL_E_2:
                return quality in [DallEImageQuality.STANDARD]
            case OpenAIModel.MODEL_DALL_E_3:
                return quality in [DallEImageQuality.STANDARD, DallEImageQuality.HD]
            case _:
                return False


class DallEImageSize(Enum):
    SIZE_256_X_256 = auto()
    SIZE_512_X_512 = auto()
    SIZE_1024_X_1024 = auto()
    SIZE_1024_X_1792 = auto()
    SIZE_1792_X_1024 = auto()

    @property
    def api_name(self) -> str:
        match self:
            case DallEImageSize.SIZE_256_X_256:
                return "256x256"
            case DallEImageSize.SIZE_512_X_512:
                return "512x512"
            case DallEImageSize.SIZE_1024_X_1024:
                return "1024x1024"
            case DallEImageSize.SIZE_1024_X_1792:
                return "1024x1792"
            case DallEImageSize.SIZE_1792_X_1024:
                return "1792x1024"
            case _:
                raise NotImplementedError

    @property
    def is_portrait(self) -> bool:
        match self:
            case DallEImageSize.SIZE_1024_X_1792:
                return True
            case _:
                return False

    @property
    def is_landscape(self) -> bool:
        match self:
            case DallEImageSize.SIZE_1792_X_1024:
                return True
            case _:
                return False

    @property
    def is_square(self) -> bool:
        match self:
            case DallEImageSize.SIZE_256_X_256 | DallEImageSize.SIZE_512_X_512 | DallEImageSize.SIZE_1024_X_1024:
                return True
            case _:
                return False


class DallEImageQuality(Enum):
    STANDARD = auto()
    HD = auto()

    @property
    def api_name(self) -> str:
        return self.name.lower()
