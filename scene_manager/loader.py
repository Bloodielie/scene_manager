import os
import importlib.util
from inspect import ismodule, ismethod

from aiogram import Dispatcher
from loguru import logger
from scene_manager.base_scenes import MessageScene, QueryScene, BaseScene
from typing import Set, Optional, Callable
from scene_manager.storages.base import BaseStorage


class SceneNotFoundError(Exception):
    pass


class Loader:
    def __init__(self,
                 dispatcher: Dispatcher,
                 storage: BaseStorage,
                 path_to_scenes: Optional[str] = None) -> None:
        self._dispatcher = dispatcher
        self._storage = storage
        self._path_to_scenes = path_to_scenes or './scenes'
        self._message_handlers = {}
        self._query_handlers = {}
        self._scenes_types = {
            MessageScene: self._message_handlers,
            QueryScene: self._query_handlers
        }
        self._default_attr = self.get_module_dir(BaseScene)
        self.class_distribution()

    def class_distribution(self) -> None:
        user_classes = self.getting_all_classes()
        for user_class in user_classes:
            user_class = user_class(self._dispatcher, self._storage)
            user_methods = self.get_user_dir(user_class)
            for scenes_type in self._scenes_types.keys():
                if not isinstance(user_class, scenes_type):
                    continue
                handler_dictionary = self._scenes_types.get(scenes_type)
                for user_method in user_methods:
                    user_attr = getattr(user_class, user_method)
                    if not ismethod(user_attr):
                        continue
                    handler_dictionary[user_method] = user_attr
                break

    def getting_all_classes(self) -> set:
        classes = set()
        files = [x.replace(".py", "") for x in os.listdir(self._path_to_scenes) if x not in ["__pycache__", "__init__.py"]]
        for file in files:
            module = self.load_module(file)
            classes.update(self.get_classes(module))
        return classes

    def get_classes(self, module) -> set:
        user_classes = set()
        module_dirs = self.get_module_dir(module)
        for module_dir in module_dirs:
            user_class = getattr(module, module_dir)
            try:
                if not ismodule(user_class) and user_class not in self._scenes_types.keys():
                    user_classes.add(user_class)
            except Exception as e:
                logger.exception(f"Error in module check: {e}")
        return user_classes

    @staticmethod
    def get_module_dir(user_object) -> Set[str]:
        return {dir_ for dir_ in dir(user_object) if not dir_.endswith('__')}

    def get_user_dir(self, user_class) -> Set[str]:
        all_dir = self.get_module_dir(user_class)
        return all_dir - self._default_attr

    def load_module(self, file_name: str):
        spec = importlib.util.spec_from_file_location(file_name, os.path.abspath(f"{self._path_to_scenes}/{file_name}.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_message_scene_callback(self, scene_name: str) -> Callable:
        callback = self._message_handlers.get(scene_name)
        if not callback:
            raise SceneNotFoundError("There is no such scene")
        return callback
