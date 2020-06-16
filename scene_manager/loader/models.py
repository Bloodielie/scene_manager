from typing import Callable, Optional
from pydantic import BaseModel

from scene_manager.scenes.samples import MessageScene, QueryScene
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
        self._query_handlers = {}
        self.scenes_types = {
            MessageScene: self._message_handlers,
            QueryScene: self._query_handlers,
        }

    def get_message_scene(self, scene_name: str) -> SceneModel:
        scene_model = self._message_handlers.get(scene_name)
        if not scene_model:
            raise SceneNotFoundError("There is no such scene")
        return scene_model

    def set_scene(self, scene_class: BaseScene, scene_name: str, scene_model: SceneModel) -> None:
        _handlers_dict = self.scenes_types.get(scene_class)
        if _handlers_dict is None:
            raise TypeError("scene class not found")
        _handlers_dict[scene_name] = scene_model
