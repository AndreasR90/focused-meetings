import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from websocket import manager

app = FastAPI()

import api.routes  # noqa isort:skip

logger = logging.getLogger(__name__)


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    group_id = "hello"
    await manager.connect(websocket=websocket, group_id=group_id)
    try:
        while True:
            data = await websocket.receive_json()
            logger.error(data)
            await manager.broadcast_single(websocket, data={"msg": "hello world"})
    except WebSocketDisconnect:
        manager.disconnect(websocket, group_id=group_id)
