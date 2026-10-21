from datetime import datetime, timedelta
from weakref import WeakValueDictionary
from sqlalchemy import select, and_, or_
from database import User, Deck
from social.models import BattleInvitation
from social.service import SocialError, lock_relation, require_friends


class BattleService:
    def __init__(self, session_factory, room_server):
        self.session_factory = session_factory
        self.room_server = room_server
        self.rooms = WeakValueDictionary()

    async def player_deck(self, session, user_id, deck_id):
        result = await session.execute(
            select(Deck.content, User.username).join(User, User.id == Deck.user_id)
            .where(Deck.id == deck_id, Deck.user_id == user_id).with_for_update()
        )
        row = result.first()
        if row is None or not row.content:
            return None
        return row.content, row.username

    async def username(self, session, user_id):
        result = await session.execute(select(User.username).where(User.id == user_id))
        return result.scalar_one()

    def check_players(self, *usernames):
        for username in usernames:
            if (
                self.room_server.check_client_in_room(username)
                or self.room_server.check_client_in_queue(username)
            ):
                raise SocialError(409, "player_busy")

    def serialize(self, invitation):
        status = invitation.status
        if status == "pending" and invitation.expires_at <= datetime.utcnow():
            status = "expired"
        room = self.rooms.get(invitation.id)
        active = status == "accepted" and room is not None and all(
            self.room_server.find_player_room(username) is room for username in room.players
        )
        return {
            "id": invitation.id,
            "sender_id": invitation.sender_id,
            "receiver_id": invitation.receiver_id,
            "status": status,
            "expires_at": invitation.expires_at,
            "active": active,
            "game_url": "/gaming" if active else None
        }

    async def create(self, actor_id, target_id, invitation_id, deck_id):
        async with self.session_factory() as session:
            async with session.begin():
                relation = await lock_relation(session, actor_id, target_id)
                previous = await session.get(BattleInvitation, invitation_id, with_for_update=True)
                if previous is not None:
                    if (
                        previous.sender_id != actor_id or previous.receiver_id != target_id
                        or previous.sender_deck_id != deck_id
                    ):
                        raise SocialError(409, "invitation_id_conflict")
                    return self.serialize(previous)

                require_friends(relation)
                player = await self.player_deck(session, actor_id, deck_id)
                if player is None:
                    raise SocialError(400, "invalid_deck")
                target_name = await self.username(session, target_id)
                self.check_players(player[1], target_name)
                pending = await session.execute(select(BattleInvitation).where(
                    BattleInvitation.status == "pending",
                    BattleInvitation.expires_at > datetime.utcnow(),
                    or_(
                        and_(BattleInvitation.sender_id == actor_id, BattleInvitation.receiver_id == target_id),
                        and_(BattleInvitation.sender_id == target_id, BattleInvitation.receiver_id == actor_id)
                    )
                ))
                if pending.scalars().first() is not None:
                    raise SocialError(409, "pending_invitation_exists")

                invitation = BattleInvitation(
                    id=invitation_id, sender_id=actor_id, receiver_id=target_id,
                    sender_deck_id=deck_id,
                    expires_at=datetime.utcnow() + timedelta(seconds=60)
                )
                session.add(invitation)
                await session.flush()
                payload = self.serialize(invitation)
        return payload

    async def list_invitations(self, actor_id, offset=0, limit=30):
        async with self.session_factory() as session:
            result = await session.execute(
                select(BattleInvitation)
                .where(or_(BattleInvitation.sender_id == actor_id, BattleInvitation.receiver_id == actor_id))
                .order_by(BattleInvitation.created_at.desc(), BattleInvitation.id)
                .offset(offset).limit(limit)
            )
            return [self.serialize(invitation) for invitation in result.scalars()]

    async def process(self, actor_id, invitation_id, action, deck_id=None):
        transitions = {"accept": "accepted", "reject": "rejected", "cancel": "cancelled"}
        if action not in transitions:
            raise ValueError("Unknown invitation action")

        # 只读取参与者；事务内按用户 ID 加锁后重新读取邀请状态。
        async with self.session_factory() as session:
            invitation = await session.get(BattleInvitation, invitation_id)
            if invitation is None:
                raise SocialError(404, "invitation_not_found")
            sender_id, receiver_id = invitation.sender_id, invitation.receiver_id

        expected_actor = sender_id if action == "cancel" else receiver_id
        if actor_id != expected_actor:
            raise SocialError(403, "cannot_process_invitation")

        room = None
        try:
            async with self.session_factory() as session:
                async with session.begin():
                    relation = await lock_relation(session, sender_id, receiver_id)
                    invitation = await session.get(BattleInvitation, invitation_id, with_for_update=True)
                    if invitation is None:
                        raise SocialError(404, "invitation_not_found")

                    next_status = transitions[action]
                    if invitation.status == next_status:
                        if action == "accept" and invitation.receiver_deck_id != deck_id:
                            raise SocialError(409, "accepted_deck_conflict")
                        return self.serialize(invitation)
                    if invitation.status != "pending":
                        raise SocialError(409, "invitation_already_processed")

                    if invitation.expires_at <= datetime.utcnow():
                        invitation.status = "expired"
                    elif action == "accept":
                        require_friends(relation)
                        sender_name = await self.username(session, sender_id)
                        receiver_name = await self.username(session, receiver_id)
                        self.check_players(sender_name, receiver_name)

                        sender = await self.player_deck(session, sender_id, invitation.sender_deck_id)
                        receiver = await self.player_deck(session, receiver_id, deck_id)
                        if sender is None or receiver is None:
                            raise SocialError(400, "invalid_deck")
                        # 卡组查询会让出执行权，开房前再次检查。
                        self.check_players(sender[1], receiver[1])
                        room = await self.room_server.create_new_room(sender, receiver)
                        self.rooms[invitation.id] = room
                        invitation.receiver_deck_id = deck_id
                        invitation.status = "accepted"
                    else:
                        invitation.status = next_status

                    await session.flush()
                    payload = self.serialize(invitation)
        except BaseException:
            if room is not None:
                self.rooms.pop(invitation_id, None)
                await self.room_server.discard_room(room)
            raise
        return payload
