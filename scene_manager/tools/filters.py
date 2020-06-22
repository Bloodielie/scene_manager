from functools import wraps
from typing import Callable, List, Union, Optional

from aiogram import types
from aiogram.types import ContentType

from scene_manager.utils import content_type_checker
from abc import ABC, abstractmethod


def context_types_filter(
    context_types: List[Union[ContentType, str]], otherwise_handler: Optional[Callable] = None
) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, message: types.Message) -> Callable:
            if content_type_checker(message, context_types):
                return await func(self, message)
            elif otherwise_handler is not None:
                return await otherwise_handler(self, message)

        return wrapper

    return decorator


def query_data_filter(data: List[str], otherwise_handler: Optional[Callable] = None) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, query: types.CallbackQuery) -> Callable:
            if isinstance(query.data, str) and query.data in data:
                return await func(self, query)
            elif isinstance(query.data, list) and set(query.data).issubset(set(data)):
                return await func(self, query)
            elif otherwise_handler is not None:
                return await otherwise_handler(self, query)

        return wrapper

    return decorator


class BaseFilter(ABC):
    @abstractmethod
    def __call__(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def otherwise_handler(self):
        raise NotImplementedError


def filter_manager(filter) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, ctx) -> Callable:
            filter_obj = filter(ctx)
            filter_result = await filter_obj()
            if filter_result:
                return await func(self, ctx)
            elif getattr(filter_obj, "otherwise_handler", None) is not None:
                return await filter_obj.otherwise_handler()

        return wrapper

    return decorator
