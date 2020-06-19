from typing import List, Union

from aiogram import types
from aiogram.types import ContentType


def content_type_checker(message: types.Message, context_types: List[Union[ContentType, str, None]]) -> bool:
    content_type = message.content_type
    if context_types is None:
        return False
    elif context_types[0] == "any":
        return True
    elif isinstance(content_type, str) and content_type in context_types:
        return True
    elif isinstance(content_type, list) and set(content_type).issubset(set(context_types)):
        return True
    else:
        return False
