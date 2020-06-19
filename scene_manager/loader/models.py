from typing import Callable, Optional, Set, Generator
from pydantic import BaseModel

from scene_manager.scenes.samples import MessageScene, CallbackQueryScene
from scene_manager.scenes.base import BaseScene


class SceneModel(BaseModel):
    scene_name: Optional[str] = None
    handler: Callable
    link_to_object: "BaseScene"
    config: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self):
        return hash((self.scene_name, self.handler, self.link_to_object))


class HandlersStorage:
    def __init__(self) -> None:
        self._message_handlers: Set[SceneModel] = set()
        self._callback_query_handler: Set[SceneModel] = set()
        self.scenes_storages = {
            MessageScene: self._message_handlers,
            CallbackQueryScene: self._callback_query_handler,
        }

    def get_message_scene(self, scene_name: str) -> Generator[SceneModel, None, None]:
        return self._scene_getter(scene_name, self._message_handlers)

    def get_callback_query_scene(self, scene_name: str) -> Generator[SceneModel, None, None]:
        return self._scene_getter(scene_name, self._callback_query_handler)

    @staticmethod
    def _scene_getter(scene_name: str, handlers_set: set) -> Generator[SceneModel, None, None]:
        for handler in handlers_set:
            if handler.scene_name != scene_name:
                continue
            yield handler

    def set_scene(self, scene_class: BaseScene, scene_model: SceneModel) -> None:
        handlers_set = self.scenes_storages.get(scene_class)
        if handlers_set is None:
            raise TypeError("scene class not found")
        handlers_set.add(scene_model)
