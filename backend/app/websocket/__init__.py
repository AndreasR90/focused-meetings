from .actions import change_focus, login, logout
from .executor import Executor
from .manager import WebSocketManager

manager = WebSocketManager()

executor = Executor()
executor.register(login)
executor.register(change_focus)
executor.register(logout)
