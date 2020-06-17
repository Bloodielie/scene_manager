from typing import Callable, Optional
from pydantic import BaseModel

from scene_manager.scenes.samples import MessageScene, CallbackQueryScene
from scene_manager.scenes.base import BaseScene


class SceneNotFoundError(Exception):
    pass


class SceneModel(BaseModel):
    handler: Callable
    link_to_object: "BaseScene"
    config: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True


class HandlersStorage:
    def __init__(self) -> None:
        self._message_handlers = {}
        self._callback_query_handler = {}
        self.scenes_types = {
            MessageScene: self._message_handlers,
            CallbackQueryScene: self._callback_query_handler,
        }

    def get_message_scene(self, scene_name: str) -> SceneModel:
        return self._scene_getter(scene_name, self._message_handlers)

    def get_callback_query_scene(self, scene_name: str) -> SceneModel:
        return self._scene_getter(scene_name, self._callback_query_handler)

    @staticmethod
    def _scene_getter(scene_name: str, handler_dict: dict) -> SceneModel:
        scene_model = handler_dict.get(scene_name)
        if not scene_model:
            raise SceneNotFoundError("There is no such scene")
        return scene_model

    def set_scene(self, scene_class: BaseScene, scene_name: str, scene_model: SceneModel) -> None:
        _handlers_dict = self.scenes_types.get(scene_class)
        if _handlers_dict is None:
            raise TypeError("scene class not found")
        _handlers_dict[scene_name] = scene_model
