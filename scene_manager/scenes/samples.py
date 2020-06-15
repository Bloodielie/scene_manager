from typing import Optional, Union, Type

from aiogram.types import ContentType

from scene_manager.scenes.base import BaseScene, SceneConfigMetaclass


class MessageScene(BaseScene, metaclass=SceneConfigMetaclass):
    class Config:
        content_types: Optional[Union[ContentType, str]] = None


class QueryScene(BaseScene):
    pass
