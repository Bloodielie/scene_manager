from aiogram import Dispatcher, types
from scene_manager.loader import Loader
from typing import Optional
from scene_manager.storages import base, redis
from scene_manager.settings.storage import StorageSettings


class Manager:
    def __init__(self,
                 dispatcher: Dispatcher,
                 path_to_scenes: Optional[str] = None,
                 default_scene: Optional[str] = None,
                 *,
                 storage: Optional[base.BaseStorage] = None,
                 storage_settings: Optional[StorageSettings] = None) -> None:
        self._default_scene = default_scene or 'home'
        self.dispatcher = dispatcher

        self._storage_settings = storage_settings or StorageSettings()
        if storage is None:
            storage = redis.RedisStorage(self._storage_settings)
        else:
            storage = storage(self._storage_settings)
        self._storage = storage

        self.loader = Loader(dispatcher, self._storage, path_to_scenes)

    async def _message_handler(self, message: types.Message) -> None:
        user_id = message.from_user.id
        user_scene = await self._storage.get(user_id)
        if user_scene is None:
            await self._storage.put(user_id, self._default_scene)
            user_scene = self._default_scene
        callback = self.loader.get_message_scene_callback(user_scene)
        await callback(message)

    def register_handlers(self) -> None:
        self.dispatcher.register_message_handler(self._message_handler)
