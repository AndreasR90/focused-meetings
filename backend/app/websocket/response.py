from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from fastapi import WebSocket

from websocket.manager import WebSocketManager


class ResponseType(Enum):
    broadcast_single = 1
    broadcast_group = 2
    broadcast_all = 3


@dataclass
class Response:
    response_method: ResponseType
    response_data: Dict[Any, Any]
    response_arguments: Dict = field(default_factory=dict)

    async def execute(self, manager: WebSocketManager, connection: WebSocket = None):
        fct = getattr(manager, self.response_method.name)
        if self.response_method == ResponseType.broadcast_single:
            self.response_arguments["connection"] = connection
        result = await fct(**self.response_arguments, data=self.response_data)
        return result


class MultipleResponse:
    def __init__(self, responses: List[Response]):
        self.responses = responses

    async def execute(self, manager: WebSocketManager, connection: WebSocket):
        for response in self.responses:
            await response.execute(manager=manager, connection=connection)
