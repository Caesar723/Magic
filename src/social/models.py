from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Index,BigInteger, Text, UniqueConstraint
from database import Base


class FriendRelation(Base):
    __tablename__ = "social_friend_relations"

    user_low_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user_high_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_id = Column(String(36), nullable=False, unique=True)
    status = Column(String(16), nullable=False)  # pending/accepted/rejected/cancelled/deleted
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("user_low_id < user_high_id", name="ck_social_friend_order"),
        CheckConstraint("requester_id IN (user_low_id, user_high_id)", name="ck_social_friend_requester"),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected', 'cancelled', 'deleted')",
            name="ck_social_friend_status"
        ),
        Index("ix_social_friend_low_status", "user_low_id", "status"),
        Index("ix_social_friend_high_status", "user_high_id", "status"),
    )

class ChatMessage(Base):
    __tablename__ = "social_chat_messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(String(36), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("sender_id", "client_id", name="uq_social_message_client"),
        Index("ix_social_message_pair", "sender_id", "receiver_id", "id"),
        Index("ix_social_message_reverse", "receiver_id", "sender_id", "id"),
        Index("ix_social_message_unread", "receiver_id", "read_at", "sender_id"),
    )


class BattleInvitation(Base):
    __tablename__ = "social_battle_invitations"

    id = Column(String(36), primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender_deck_id = Column(Integer, nullable=False)
    receiver_deck_id = Column(Integer, nullable=True)
    status = Column(String(16), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint("sender_id != receiver_id", name="ck_social_battle_users"),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected', 'cancelled', 'expired', 'failed')",
            name="ck_social_battle_status"
        ),
        Index("ix_social_battle_sender", "sender_id", "created_at"),
        Index("ix_social_battle_receiver", "receiver_id", "created_at"),
    )