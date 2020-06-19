from typing import Optional

from aiogram import Dispatcher, Bot
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
    def __init__(self, storage: BaseStorage, dispatcher: Optional[Dispatcher] = None) -> None:
        self.dispatcher = dispatcher or Dispatcher.get_current()
        self.storage = storage
        if self.dispatcher is None:
            bot = None
        else:
            bot = self.dispatcher.bot
        self.bot = bot

    def __getattribute__(self, name: str):
        attr = super().__getattribute__(name)
        if name == "bot" and attr is None:
            bot = Bot.get_current()
            super().__setattr__(name, bot)
            return bot
        if name == "dispatcher" and attr is None:
            dispatcher = Dispatcher.get_current()
            super().__setattr__(name, dispatcher)
            return dispatcher
        return attr

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
