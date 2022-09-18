from typing import Dict, List

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: List[WebSocket] = []
        self._grouped_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group_id: str):
        await websocket.accept()
        self._connections.append(websocket)
        self._add_grouped_connection(websocket=websocket, group_id=group_id)

    def disconnect(self, websocket: WebSocket, group_id: str):
        self._connections.remove(websocket)
        self._remove_grouped_connection(websocket=websocket, group_id=group_id)

    async def broadcast_single(self, connection: WebSocket, data: Dict):
        await self._send_to_connection(connection=connection, data=data)

    async def broadcast_group(self, group_id: str, data: Dict):
        for connection in self._grouped_connections.get(group_id, []):
            await self._send_to_connection(connection=connection, data=data)

    async def broadcast_all(self, data: Dict):
        for conneciton in self._connections:
            await self._send_to_connection(connection=conneciton, data=data)

    def _add_grouped_connection(self, websocket: WebSocket, group_id: str):
        if group_id not in self._grouped_connections:
            self._grouped_connections[group_id] = []
        self._grouped_connections[group_id].append(websocket)

    def _remove_grouped_connection(self, websocket: WebSocket, group_id: str):
        self._grouped_connections[group_id].remove(websocket)
        if len(self._grouped_connections[group_id]) == 0:
            del self._grouped_connections[group_id]

    async def _send_to_connection(self, connection: WebSocket, data: Dict):
        await connection.send_json(data)
