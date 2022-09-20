import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from db.init_db import init_db
from websocket import executor, manager
from websocket.executor import Request

app = FastAPI()

import api.routes  # noqa isort:skip

logger = logging.getLogger(__name__)


@app.on_event("startup")
def startup():
    init_db()


@app.websocket("/ws/{session_id}")
async def websocket(websocket: WebSocket, session_id: str):
    user_id = None
    await manager.connect(websocket=websocket, group_id=session_id)
    try:
        while True:
            data = await websocket.receive_json()
            request = Request.from_dict(data)
            return_data = executor.execute(request=request)
            if request.function == "login":
                user_id = list(filter(lambda x: x.response_data["event"] == "user_id", return_data.responses,))[
                    0
                ].response_data["data"]
            await return_data.execute(manager=manager, connection=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, group_id=session_id)
        if user_id is not None:
            return_data = executor.execute(
                Request(function="logout", arguments=dict(id=user_id, session_id=session_id))
            )
            await return_data.execute(manager=manager, connection=websocket)
    except Exception as e:
        logger.error(e)
        raise e


@app.get("/")
def index():
    return "Hello"
