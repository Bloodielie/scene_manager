from typing import Any, Optional

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from scene_manager.exceptions import LoaderNotInitError
from scene_manager.loader.loader import Loader
from scene_manager.utils import content_type_checker


class ScenesMiddleware(BaseMiddleware):
    def __init__(self, *, loader: Optional[Loader] = None, default_scene_name: Optional[str] = None):
        self._default_scene_name = default_scene_name or "start"
        self._loader = loader or Loader.get_current()
        if self._loader is None:
            raise LoaderNotInitError("Inoculate the loader")
        if not self._loader.is_scenes_loaded:
            self._loader.load_scenes()
        self._storage = self._loader.storage
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_scene_name = await self._get_scene_name(message)
        scene_model = self._loader.get_message_scene_model(user_scene_name)
        if content_type_checker(message, scene_model.config.get("content_types")):
            await scene_model.handler(message)
            raise CancelHandler()
        else:
            otherwise_handler = scene_model.config.get("otherwise_handler")
            if otherwise_handler is not None:
                await otherwise_handler(message)

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user_scene_name = await self._get_scene_name(callback_query)
        scene_model = self._loader.get_callback_query_scene_model(user_scene_name)
        await scene_model.handler(callback_query)
        raise CancelHandler()

    async def _get_scene_name(self, ctx) -> Any:
        user_id = ctx.from_user.id
        user_scene = await self._storage.get(user_id)
        if user_scene is None:
            await self._storage.put(user_id, self._default_scene_name)
            user_scene = self._default_scene_name
        return user_scene
