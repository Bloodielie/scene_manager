from typing import Optional, Union

from aiogram.types import ContentType

from scene_manager.scenes.base import BaseScene


class MessageScene(BaseScene):
    class Config:
        content_types: Optional[Union[ContentType, str]] = [ContentType.ANY]


class QueryScene(BaseScene):
    pass
