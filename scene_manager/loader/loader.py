from inspect import ismodule, ismethod
from typing import Optional, Set

from aiogram import Dispatcher

from scene_manager.loader import utils
from scene_manager.loader.models import HandlersStorage, SceneModel
from scene_manager.loader.utils import get_class_attr
from scene_manager.scenes.base import BaseScene
from scene_manager.storages.base import BaseStorage
from loguru import logger


def get_user_attr(user_class) -> Set[str]:
    all_dir = get_class_attr(user_class)
    return all_dir - get_class_attr(BaseScene)


class Loader:
    def __init__(self, dispatcher: Dispatcher, storage: BaseStorage, path_to_scenes: Optional[str] = None) -> None:
        self._dispatcher = dispatcher
        self._storage = storage
        self._path_to_scenes = path_to_scenes or "./scenes"
        self._handlers_storage = HandlersStorage()

    def load_scenes(self) -> None:
        self._class_distribution()

    def _class_distribution(self) -> None:
        logger.debug("Start load scenes")
        user_classes = self._loading_classes()
        for user_class in user_classes:
            user_class = user_class(self._dispatcher, self._storage)
            self._recording_scenes_from_types(user_class)

    def _recording_scenes_from_types(self, user_class) -> None:
        user_methods = get_user_attr(user_class)
        for scenes_type in self._handlers_storage.scenes_types.keys():
            if not isinstance(user_class, scenes_type):
                continue
            for user_method in user_methods:
                user_attr = getattr(user_class, user_method)
                if not ismethod(user_attr):
                    continue
                scene_model = SceneModel(handler=user_attr, link_to_object=user_class, config=user_class.config)
                self._handlers_storage.set_scene(scenes_type, user_method, scene_model)
                logger.debug(f"Add scene {scenes_type}, {user_method}, {scene_model}")
            break

    def _loading_classes(self) -> set:
        classes = set()
        files_path = utils.recursive_load_files(self._path_to_scenes)
        for file_path in files_path:
            module = utils.load_module(file_path)
            classes.update(self._get_classes(module))
        return classes

    def _get_classes(self, module) -> set:
        user_classes = set()
        module_dirs = utils.get_class_attr(module)
        for module_dir in module_dirs:
            user_class = getattr(module, module_dir)
            try:
                if not ismodule(user_class) and user_class not in self._handlers_storage.scenes_types.keys():
                    user_classes.add(user_class)
            except Exception as e:
                logger.exception(f"Error in module check: {e}")
        return user_classes

    def get_message_scene_model(self, scene_name: str) -> SceneModel:
        return self._handlers_storage.get_message_scene(scene_name)

    def get_callback_query_scene_model(self, scene_name: str) -> SceneModel:
        return self._handlers_storage.get_callback_query_scene(scene_name)
