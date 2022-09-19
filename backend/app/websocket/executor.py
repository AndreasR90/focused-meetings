from typing import Callable, Dict, Optional

from websocket.request import Request
from websocket.response import Response


class Executor:
    def __init__(self) -> None:
        self.registered_functions: Dict[str, Callable] = {}

    def register(self, function: Callable, name: Optional[str] = None):
        used_name = name or function.__name__
        self.registered_functions[used_name] = function

    def execute(self, request: Request) -> Response:
        fct = self.registered_functions.get(request.function)
        if fct is None:
            raise AttributeError(f"Function {request.function} is not registered")
        return fct(**request.arguments)
