from inspect import ismodule, ismethod
from typing import Optional, Set, Union, List

from aiogram import Dispatcher

from scene_manager import StorageSettings
from scene_manager.loader import utils
from scene_manager.loader.models import HandlersStorage, SceneModel
from scene_manager.loader.utils import get_class_attr
from scene_manager.scenes.base import BaseScene
from scene_manager.storages import redis
from scene_manager.storages.base import BaseStorage
from loguru import logger
from aiogram.utils.mixins import ContextInstanceMixin
from functools import lru_cache


@lru_cache
def get_user_attr(user_class) -> Set[str]:
    all_dir = get_class_attr(user_class)
    return all_dir - get_class_attr(BaseScene)


class Loader(ContextInstanceMixin):
    def __init__(
        self,
        *,
        dispatcher: Optional[Dispatcher] = None,
        storage: Optional[BaseStorage] = None,
        path_to_scenes: Optional[Union[str, List[str]]] = None,
    ) -> None:
        self._dispatcher = dispatcher
        self.data_storage = storage or redis.RedisStorage(StorageSettings())
        self.handlers_storage = HandlersStorage()
        self.is_scenes_loaded = False

        if path_to_scenes is None:
            path_to_scenes = ["./scenes"]
        elif isinstance(path_to_scenes, str):
            path_to_scenes = [path_to_scenes]
        self._path_to_scenes = path_to_scenes

        self.set_current(self)

    def load_scenes(self) -> None:
        self.is_scenes_loaded = True
        self._class_distribution()

    def _class_distribution(self) -> None:
        logger.debug("Start load scenes")
        for user_class in self._loading_classes():
            user_class = user_class(self.data_storage, dispatcher=self._dispatcher)
            self._recording_scene(user_class)

    def _recording_scene(self, user_class) -> None:
        scene_storage = self._find_scene_storage(user_class)
        for user_method in get_user_attr(user_class):
            user_attr = getattr(user_class, user_method)
            if not ismethod(user_attr):
                continue
            scene_model = SceneModel(
                scene_name=user_method, handler=user_attr, link_to_object=user_class, config=user_class.config
            )
            self.handlers_storage.set_scene(scene_storage, scene_model)
            logger.debug(f"Add scene {scene_storage}, {user_method}, {scene_model}")

    def _find_scene_storage(self, user_class):
        for scenes_type in self.handlers_storage.scenes_storages.keys():
            if not isinstance(user_class, scenes_type):
                continue
            return scenes_type

    def _loading_classes(self) -> list:
        classes = list()
        files_path = list()
        for directory in self._path_to_scenes:
            files_path.extend(utils.recursive_load_files(directory))
        for file_path in files_path:
            module = utils.load_module(file_path)
            classes.extend(self._get_classes(module))
        return classes

    def _get_classes(self, module) -> list:
        user_classes = list()
        module_dirs = utils.get_class_attr(module)
        for module_dir in module_dirs:
            user_class = getattr(module, module_dir)
            try:
                if not ismodule(user_class) and user_class not in self.handlers_storage.scenes_storages.keys():
                    user_classes.append(user_class)
            except Exception as e:
                logger.exception(f"Error in module check: {e}")
        return user_classes
