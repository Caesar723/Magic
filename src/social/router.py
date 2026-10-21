import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from uuid import UUID
from urllib.parse import urlsplit
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from database import User
from server_function_tool import get_current_user
from social.service import FriendService, SocialError
from social.chat import ChatService
from social.battle import BattleService


class CreateFriendRequest(BaseModel):
    target_user_id: int = Field(gt=0)


class ProcessFriendRequest(BaseModel):
    request_id: UUID


class SendChatMessage(BaseModel):
    client_id: UUID
    content: str = Field(min_length=1, max_length=2000)


class ReadChatMessages(BaseModel):
    last_message_id: int = Field(gt=0)


class CreateBattleInvitation(BaseModel):
    invitation_id: UUID
    target_user_id: int = Field(gt=0)
    deck_id: int = Field(gt=0)


class AcceptBattleInvitation(BaseModel):
    deck_id: int = Field(gt=0)


def get_social_router(database, connections, room_server):
    router = APIRouter(prefix="/social", tags=["social"])
    service = FriendService(database.AsyncSessionLocal)
    chat = ChatService(database.AsyncSessionLocal)
    battle = BattleService(database.AsyncSessionLocal, room_server)
    legacy_auth = get_current_user(database)

    async def resolve_user_id(connection):
        if not connection.cookies.get("mycookie"):
            raise HTTPException(401, detail={"code": "authentication_required"})

        try:
            username = await legacy_auth(connection)
        except (ValueError, TypeError, KeyError):
            raise HTTPException(401, detail={"code": "invalid_authentication"}) from None

        if isinstance(username, RedirectResponse) or not isinstance(username, str):
            raise HTTPException(401, detail={"code": "authentication_required"})

        async with database.AsyncSessionLocal() as session:
            result = await session.execute(select(User.id).where(User.username == username))
            try:
                user_id = result.scalar_one_or_none()
            except MultipleResultsFound:
                raise HTTPException(409, detail={"code": "ambiguous_account"}) from None

        if user_id is None:
            raise HTTPException(401, detail={"code": "authentication_required"})
        return user_id

    async def current_user_id(request: Request):
        return await resolve_user_id(request)

    async def execute(operation):
        try:
            return await operation
        except SocialError as error:
            raise HTTPException(error.status_code, detail={"code": error.code}) from None

    async def notify_users(event, *user_ids):
        event = jsonable_encoder(event)
        await asyncio.gather(*(
            connections.push(user_id, event) for user_id in set(user_ids)
        ))

    @router.post("/friend-requests")
    async def send_request(body: CreateFriendRequest, actor_id: int = Depends(current_user_id)):
        result = await execute(service.send_request(actor_id, body.target_user_id))
        await notify_users({"type": "friend.changed"}, actor_id, body.target_user_id)
        return result

    @router.get("/friend-requests/incoming")
    async def incoming_requests(
        actor_id: int = Depends(current_user_id),
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=30, ge=1, le=100)
    ):
        return await service.list_relations(actor_id, "incoming", offset, limit)

    @router.get("/friend-requests/outgoing")
    async def outgoing_requests(
        actor_id: int = Depends(current_user_id),
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=30, ge=1, le=100)
    ):
        return await service.list_relations(actor_id, "outgoing", offset, limit)


    @router.get("/friends")
    async def list_friends(
        actor_id: int = Depends(current_user_id),
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=30, ge=1, le=100)
    ):
        return await service.list_relations(actor_id, "friends", offset, limit)


    @router.websocket("/ws")
    async def social_socket(websocket: WebSocket):
        try:
            origin = urlsplit(websocket.headers.get("origin", ""))
        except ValueError:
            await websocket.close(code=1008)
            return
        scheme = "https" if websocket.url.scheme == "wss" else "http"
        if origin.scheme != scheme or origin.netloc != websocket.url.netloc:
            await websocket.close(code=1008)
            return

        try:
            user_id = await resolve_user_id(websocket)
        except HTTPException:
            await websocket.close(code=1008)
            return

        connection = await connections.connect(user_id, websocket)
        try:
            if not await connections.send(user_id, connection, {"type": "connected"}):
                return

            while True:
                # 前端每 20 秒发送一次 {"type": "ping"}。
                data = await asyncio.wait_for(websocket.receive_json(), timeout=45)
                if not isinstance(data, dict) or data.get("type") != "ping":
                    await websocket.close(code=1008)
                    break

                if not await connections.send(user_id, connection, {"type": "pong"}):
                    break
        except (WebSocketDisconnect, asyncio.TimeoutError, ValueError):
            pass
        finally:
            await connections.close(user_id, connection)

    @router.post("/friend-requests/{target_id}/accept")
    async def accept_request(
        target_id: int, body: ProcessFriendRequest,
        actor_id: int = Depends(current_user_id)
    ):
        result = await execute(
            service.process_request(actor_id, target_id, str(body.request_id), "accept")
        )
        await notify_users({"type": "friend.changed"}, actor_id, target_id)
        return result

    @router.post("/friend-requests/{target_id}/reject")
    async def reject_request(
        target_id: int, body: ProcessFriendRequest,
        actor_id: int = Depends(current_user_id)
    ):
        result = await execute(
            service.process_request(actor_id, target_id, str(body.request_id), "reject")
        )
        await notify_users({"type": "friend.changed"}, actor_id, target_id)
        return result

    @router.post("/friend-requests/{target_id}/cancel")
    async def cancel_request(
        target_id: int, body: ProcessFriendRequest,
        actor_id: int = Depends(current_user_id)
    ):
        result = await execute(
            service.process_request(actor_id, target_id, str(body.request_id), "cancel")
        )
        await notify_users({"type": "friend.changed"}, actor_id, target_id)
        return result

    @router.delete("/friends/{target_id}")
    async def delete_friend(target_id: int, actor_id: int = Depends(current_user_id)):
        result = await execute(service.delete_friend(actor_id, target_id))
        await notify_users({"type": "friend.changed"}, actor_id, target_id)
        return result

    @router.get("/users")
    async def search_users(
        keyword: str = Query(min_length=1, max_length=64),
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=20, ge=1, le=50),
        actor_id: int = Depends(current_user_id)
    ):
        return await service.search_users(actor_id, keyword, offset, limit)

    @router.post("/chats/{target_id}/messages")
    async def send_chat_message(
        target_id: int, body: SendChatMessage,
        actor_id: int = Depends(current_user_id)
    ):
        result = await execute(chat.send(actor_id, target_id, str(body.client_id), body.content))
        await notify_users({"type": "chat.message", "data": result}, actor_id, target_id)
        return result

    @router.get("/chats/{target_id}/messages")
    async def chat_history(
        target_id: int,
        before_id: int = Query(default=None, gt=0),
        after_id: int = Query(default=None, gt=0),
        limit: int = Query(default=30, ge=1, le=100),
        actor_id: int = Depends(current_user_id)
    ):
        return await execute(chat.history(actor_id, target_id, before_id, after_id, limit))

    @router.get("/chats/unread")
    async def unread_messages(actor_id: int = Depends(current_user_id)):
        return await chat.unread(actor_id)

    @router.post("/chats/{target_id}/read")
    async def read_chat_messages(
        target_id: int, body: ReadChatMessages,
        actor_id: int = Depends(current_user_id)
    ):
        result = await execute(chat.mark_read(actor_id, target_id, body.last_message_id))
        await notify_users({
            "type": "chat.read",
            "data": {
                "reader_id": actor_id, "peer_id": target_id,
                "last_message_id": body.last_message_id
            }
        }, actor_id, target_id)
        return result

    @router.post("/battle-invitations")
    async def create_battle_invitation(
        body: CreateBattleInvitation, actor_id: int = Depends(current_user_id)
    ):
        result = await execute(battle.create(
            actor_id, body.target_user_id, str(body.invitation_id), body.deck_id
        ))
        await notify_users(
            {"type": "battle.invitation.changed", "data": result},
            actor_id, body.target_user_id
        )
        return result

    @router.get("/battle-invitations")
    async def list_battle_invitations(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=30, ge=1, le=100),
        actor_id: int = Depends(current_user_id)
    ):
        return await battle.list_invitations(actor_id, offset, limit)

    async def process_battle(actor_id, invitation_id, action, deck_id=None):
        result = await execute(battle.process(actor_id, str(invitation_id), action, deck_id))
        event_type = "battle.ready" if result["active"] else "battle.invitation.changed"
        await notify_users(
            {"type": event_type, "data": result}, result["sender_id"], result["receiver_id"]
        )
        return result

    @router.post("/battle-invitations/{invitation_id}/accept")
    async def accept_battle_invitation(
        invitation_id: UUID, body: AcceptBattleInvitation,
        actor_id: int = Depends(current_user_id)
    ):
        return await process_battle(actor_id, invitation_id, "accept", body.deck_id)

    @router.post("/battle-invitations/{invitation_id}/reject")
    async def reject_battle_invitation(
        invitation_id: UUID, actor_id: int = Depends(current_user_id)
    ):
        return await process_battle(actor_id, invitation_id, "reject")

    @router.post("/battle-invitations/{invitation_id}/cancel")
    async def cancel_battle_invitation(
        invitation_id: UUID, actor_id: int = Depends(current_user_id)
    ):
        return await process_battle(actor_id, invitation_id, "cancel")

    return router
