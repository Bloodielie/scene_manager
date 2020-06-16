from typing import Optional

from aiogram import Dispatcher
from aiogram.types.base import TelegramObject

from scene_manager.loader.utils import get_class_attr
from scene_manager.storages.base import BaseStorage


class SceneConfigMetaclass(type):
    def __init__(cls, class_name: str, parents: tuple, attributes: dict) -> None:
        if not parents:
            super().__init__(class_name, parents, attributes)
            return

        new_config = attributes.get("Config")
        if new_config is None:
            super().__init__(class_name, parents, attributes)
            return

        for parent in parents:
            old_config = getattr(parent, "Config")
            for user_attr in get_class_attr(old_config):
                try:
                    getattr(new_config, user_attr)
                except AttributeError:
                    setattr(new_config, user_attr, getattr(old_config, user_attr))

        super().__init__(class_name, parents, attributes)


class BaseScene(metaclass=SceneConfigMetaclass):
    def __init__(self, dispatcher: Dispatcher, storage: BaseStorage) -> None:
        self.dispatcher = dispatcher
        self.storage = storage
        self.bot = self.dispatcher.bot

    async def set_scene(self, ctx: TelegramObject, scene_name: str) -> None:
        await self.storage.put(ctx.from_user.id, scene_name)

    class Config:
        pass

    @property
    def config(self) -> Optional[dict]:
        dict_ = {}
        all_dir = get_class_attr(getattr(self, "Config"))
        user_attrs = all_dir - get_class_attr(BaseScene)
        for user_attr in user_attrs:
            dict_[user_attr] = getattr(self.Config, user_attr)
        return dict_
