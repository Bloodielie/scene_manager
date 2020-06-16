from functools import wraps
from typing import Callable, List, Union, Optional

from aiogram import types
from aiogram.types import ContentType


def context_type_filter(
    context_types: List[Union[ContentType, str]],
    otherwise_handler: Optional[Callable] = None,
) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, message: types.Message) -> Callable:
            content_type = message.content_type
            if isinstance(content_type, str) and content_type in context_types:
                return await func(self, message)
            elif isinstance(content_type, list) and set(content_type).issubset(set(context_types)):
                return await func(self, message)
            elif otherwise_handler is not None:
                return await otherwise_handler(self, message)

        return wrapper

    return decorator
