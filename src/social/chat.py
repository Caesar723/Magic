from datetime import datetime
from sqlalchemy import select, update, and_, or_, func
from social.models import ChatMessage
from social.service import SocialError, lock_relation, require_friends


class ChatService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @staticmethod
    def serialize(message):
        return {
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "client_id": message.client_id,
            "content": message.content,
            "created_at": message.created_at,
            "read_at": message.read_at
        }

    async def send(self, actor_id, target_id, client_id, content):
        content = content.strip()
        if not content or len(content) > 2000:
            raise SocialError(400, "invalid_message")

        async with self.session_factory() as session:
            async with session.begin():
                relation = await lock_relation(session, actor_id, target_id)
                result = await session.execute(select(ChatMessage).where(
                    ChatMessage.sender_id == actor_id, ChatMessage.client_id == client_id
                ))
                previous = result.scalar_one_or_none()

                if previous is not None:
                    if previous.receiver_id != target_id or previous.content != content:
                        raise SocialError(409, "client_id_conflict")
                    return self.serialize(previous)

                require_friends(relation)
                message = ChatMessage(
                    sender_id=actor_id, receiver_id=target_id,
                    client_id=client_id, content=content
                )
                session.add(message)
                await session.flush()
                payload = self.serialize(message)

        return payload

    async def history(self, actor_id, target_id, before_id=None, after_id=None, limit=30):
        if before_id is not None and after_id is not None:
            raise SocialError(400, "invalid_cursor")

        statement = select(ChatMessage).where(or_(
            and_(ChatMessage.sender_id == actor_id, ChatMessage.receiver_id == target_id),
            and_(ChatMessage.sender_id == target_id, ChatMessage.receiver_id == actor_id)
        ))
        if after_id is not None:
            statement = statement.where(ChatMessage.id > after_id).order_by(ChatMessage.id)
        else:
            if before_id is not None:
                statement = statement.where(ChatMessage.id < before_id)
            statement = statement.order_by(ChatMessage.id.desc())

        async with self.session_factory() as session:
            result = await session.execute(statement.limit(limit))
            messages = list(result.scalars())
            if after_id is None:
                messages.reverse()
            return [self.serialize(message) for message in messages]

    async def unread(self, actor_id):
        async with self.session_factory() as session:
            result = await session.execute(
                select(ChatMessage.sender_id, func.count(ChatMessage.id).label("count"))
                .where(ChatMessage.receiver_id == actor_id, ChatMessage.read_at.is_(None))
                .group_by(ChatMessage.sender_id)
            )
            return [{"user_id": row.sender_id, "count": row.count} for row in result.all()]

    async def mark_read(self, actor_id, target_id, last_message_id):
        async with self.session_factory() as session:
            async with session.begin():
                await lock_relation(session, actor_id, target_id)
                message = await session.get(ChatMessage, last_message_id)

                if message is None:
                    raise SocialError(404, "message_not_found")
                if {message.sender_id, message.receiver_id} != {actor_id, target_id}:
                    raise SocialError(403, "message_not_in_conversation")

                result = await session.execute(
                    update(ChatMessage).where(
                        ChatMessage.receiver_id == actor_id,
                        ChatMessage.sender_id == target_id,
                        ChatMessage.id <= last_message_id,
                        ChatMessage.read_at.is_(None)
                    ).values(read_at=datetime.utcnow())
                )
                count = result.rowcount

        return {"updated": count, "last_message_id": last_message_id}
