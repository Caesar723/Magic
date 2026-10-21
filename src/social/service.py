from datetime import datetime
from uuid import uuid4
from sqlalchemy import select, case, or_
from database import User
from social.models import FriendRelation


class SocialError(Exception):
    def __init__(self, status_code, code):
        super().__init__(code)
        self.status_code = status_code
        self.code = code


async def lock_relation(session, actor_id, target_id):
    if actor_id == target_id:
        raise SocialError(400, "invalid_target")

    for user_id in sorted((actor_id, target_id)):
        result = await session.execute(select(User.id).where(User.id == user_id).with_for_update())
        if result.scalar_one_or_none() is None:
            raise SocialError(404, "user_not_found")
    return await session.get(FriendRelation, tuple(sorted((actor_id, target_id))))


def require_friends(relation):
    if relation is None or relation.status != "accepted":
        raise SocialError(403, "not_friends")


class FriendService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    @staticmethod
    def serialize(relation):
        return {
            "user_low_id": relation.user_low_id,
            "user_high_id": relation.user_high_id,
            "requester_id": relation.requester_id,
            "request_id": relation.request_id,
            "status": relation.status,
            "updated_at": relation.updated_at
        }

    @staticmethod
    def check_target(actor_id, target_id):
        if actor_id == target_id:
            raise SocialError(400, "cannot_add_self")

    async def send_request(self, actor_id, target_id):
        self.check_target(actor_id, target_id)

        async with self.session_factory() as session:
            async with session.begin():
                relation = await lock_relation(session, actor_id, target_id)
                if relation is not None:
                    if relation.status == "accepted":
                        raise SocialError(409, "already_friends")
                    if relation.status == "pending":
                        if relation.requester_id == actor_id:
                            return self.serialize(relation)
                        raise SocialError(409, "incoming_request_exists")

                if relation is None:
                    low_id, high_id = sorted((actor_id, target_id))
                    relation = FriendRelation(user_low_id=low_id, user_high_id=high_id)
                    session.add(relation)

                relation.requester_id = actor_id
                relation.request_id = str(uuid4())
                relation.status = "pending"
                relation.updated_at = datetime.utcnow()
                await session.flush()
                payload = self.serialize(relation)

        return payload

    async def process_request(self, actor_id, target_id, request_id, action):
        self.check_target(actor_id, target_id)
        transitions = {"accept": "accepted", "reject": "rejected", "cancel": "cancelled"}
        if action not in transitions:
            raise ValueError("Unknown request action")

        async with self.session_factory() as session:
            async with session.begin():
                relation = await lock_relation(session, actor_id, target_id)
                if relation is None:
                    raise SocialError(404, "request_not_found")
                if relation.request_id != request_id:
                    raise SocialError(409, "stale_request")

                is_requester = relation.requester_id == actor_id
                if action == "cancel":
                    if not is_requester:
                        raise SocialError(403, "only_requester_can_cancel")
                elif is_requester:
                    raise SocialError(403, "cannot_process_own_request")

                next_status = transitions[action]
                if relation.status == next_status:
                    return self.serialize(relation)
                if relation.status != "pending":
                    raise SocialError(409, "request_already_processed")

                relation.status = next_status
                relation.updated_at = datetime.utcnow()
                await session.flush()
                payload = self.serialize(relation)

        return payload

    async def delete_friend(self, actor_id, target_id):
        self.check_target(actor_id, target_id)

        async with self.session_factory() as session:
            async with session.begin():
                relation = await lock_relation(session, actor_id, target_id)
                if relation is None:
                    raise SocialError(404, "friend_not_found")
                if relation.status == "deleted":
                    return {"status": "deleted"}
                if relation.status != "accepted":
                    raise SocialError(409, "not_friends")

                relation.status = "deleted"
                relation.updated_at = datetime.utcnow()
                await session.flush()

        return {"status": "deleted"}

    async def list_relations(self, actor_id, kind, offset=0, limit=30):
        other_user_id = case(
            (FriendRelation.user_low_id == actor_id, FriendRelation.user_high_id),
            else_=FriendRelation.user_low_id
        )
        statement = select(FriendRelation, User).join(User, User.id == other_user_id).where(or_(
            FriendRelation.user_low_id == actor_id, FriendRelation.user_high_id == actor_id
        ))
        if kind == "friends":
            statement = statement.where(FriendRelation.status == "accepted")
        elif kind == "incoming":
            statement = statement.where(
                FriendRelation.status == "pending", FriendRelation.requester_id != actor_id
            )
        elif kind == "outgoing":
            statement = statement.where(
                FriendRelation.status == "pending", FriendRelation.requester_id == actor_id
            )
        else:
            raise ValueError("Unknown relation list kind")

        async with self.session_factory() as session:
            result = await session.execute(statement.order_by(User.id).offset(offset).limit(limit))
            return [{
                "user_id": user.id,
                "username": user.username,
                "request_id": relation.request_id,
                "status": relation.status,
                "updated_at": relation.updated_at
            } for relation, user in result.all()]

    async def search_users(self, actor_id, keyword, offset=0, limit=20):
        keyword = keyword.strip()
        if not keyword:
            return []

        async with self.session_factory() as session:
            result = await session.execute(
                select(User.id, User.username)
                .where(User.id != actor_id, User.username.contains(keyword, autoescape=True))
                .order_by(User.id).offset(offset).limit(limit)
            )
            return [{"user_id": row.id, "username": row.username} for row in result.all()]
