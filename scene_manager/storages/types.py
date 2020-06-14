from typing import Callable, Any

JSONEncoder = Callable[[Any], str]
JSONDecoder = Callable[[str], Any]
