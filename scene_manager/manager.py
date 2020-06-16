from typing import Optional, Any

from aiogram import Dispatcher, types
from aiogram.types.message import ContentType

from scene_manager.loader.loader import Loader
from scene_manager.settings.storage import StorageSettings
from scene_manager.storages import base, redis
from scene_manager.utils import content_type_checker


class Manager:
    def __init__(
        self,
        dispatcher: Dispatcher,
        path_to_scenes: Optional[str] = None,
        default_scene: Optional[str] = None,
        *,
        storage: Optional[base.BaseStorage] = None,
        storage_settings: Optional[StorageSettings] = None
    ) -> None:
        self._default_scene = default_scene or "home"
        self.dispatcher = dispatcher

        self._storage_settings = storage_settings or StorageSettings()
        if storage is None:
            storage = redis.RedisStorage(self._storage_settings)
        else:
            storage = storage(self._storage_settings)
        self._storage = storage

        self.loader = Loader(dispatcher, self._storage, path_to_scenes)

    async def _message_handler(self, message: types.Message) -> None:
        user_scene = await self.get_state_name(message)
        scene_model = self.loader.get_message_scene_callback(user_scene)
        if content_type_checker(message, scene_model.config.get("content_types")):
            await scene_model.handler(message)
        else:
            otherwise_handler = scene_model.config.get("otherwise_handler")
            if otherwise_handler is not None:
                otherwise_handler(message)

    async def get_state_name(self, ctx) -> Any:
        user_id = ctx.from_user.id
        user_scene = await self._storage.get(user_id)
        if user_scene is None:
            await self._storage.put(user_id, self._default_scene)
            user_scene = self._default_scene
        return user_scene

    def register_handlers(self) -> None:
        self.register_message_handlers(content_types=ContentType.ANY)

    def register_message_handlers(self, **kwargs) -> None:
        self.dispatcher.register_message_handler(self._message_handler, **kwargs)
