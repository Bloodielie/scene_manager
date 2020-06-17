from functools import wraps
from typing import Callable, List, Union, Optional

from aiogram import types
from aiogram.types import ContentType

from scene_manager.utils import content_type_checker


def context_type_filter(
    context_types: List[Union[ContentType, str]],
    otherwise_handler: Optional[Callable] = None,
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
