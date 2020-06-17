from glob import glob
import importlib.util
import os
from typing import Set
from loguru import logger


def load_module(file_path: str):
    file_name = file_path.split("\\")[-1:][0]
    file_path = os.path.abspath(file_path)
    logger.debug(f"Load module: {file_name}, {file_path}")
    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_class_attr(class_) -> Set[str]:
    return {dir_ for dir_ in dir(class_) if not dir_.endswith("__")}


def recursive_load_files(path: str) -> set:
    result = set()

    for walk in os.walk(path):
        for file_name in glob(os.path.join(walk[0], "*.py")):
            if file_name.endswith("__init__.py"):
                continue
            result.add(file_name)
    logger.debug(f"Found Files: {result}")
    return result
