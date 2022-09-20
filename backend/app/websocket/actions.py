from crud import (
    create_user,
    delete_user,
    get_or_create_session,
    get_users,
    toggle_focus,
)
from models.user import User
from websocket.response import MultipleResponse, Response, ResponseType

user_includes = set(["name", "focused", "id"])


def map_users(users):
    return [user.dict(include=user_includes) for user in users]


def login(name: str, session_id: str) -> MultipleResponse:
    session = get_or_create_session(session_id=session_id)
    user = User(name=name, session_id=session.id)
    create_user(user=user)
    users = get_users(session_id=session_id)
    response_users = map_users(users)
    user_response = Response(
        response_method=ResponseType.broadcast_single,
        response_data={"event": "user_id", "data": user.id},
    )
    group_response = Response(
        response_method=ResponseType.broadcast_group,
        response_data={"event": "user_update", "data": response_users},
        response_arguments=dict(group_id=session_id),
    )
    return MultipleResponse(responses=[user_response, group_response])


def change_focus(id: str, session_id: str) -> MultipleResponse:
    _ = toggle_focus(id=id)
    users = get_users(session_id=session_id)
    response_users = map_users(users)
    group_response = Response(
        response_method=ResponseType.broadcast_group,
        response_data={"event": "user_update", "data": response_users},
        response_arguments=dict(group_id=session_id),
    )
    return MultipleResponse(responses=[group_response])


def logout(id: str, session_id: str) -> MultipleResponse:
    delete_user(id=id)

    users = get_users(session_id=session_id)
    response_users = map_users(users)

    group_response = Response(
        response_method=ResponseType.broadcast_group,
        response_data={"event": "user_update", "data": response_users},
        response_arguments=dict(group_id=session_id),
    )
    return MultipleResponse(responses=[group_response])
