import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(Text)
    password_hash: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    pots_created = relationship("Pot", back_populates="creator")
    participations = relationship("Participant", back_populates="user")


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (Index("idx_matches_status", "status"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[int | None] = mapped_column(Integer, unique=True)
    home_team: Mapped[str | None] = mapped_column(Text)
    away_team: Mapped[str | None] = mapped_column(Text)
    match_date: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Text, default="upcoming")
    result: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    pots = relationship("Pot", back_populates="match")


class Pot(Base):
    __tablename__ = "pots"
    __table_args__ = (
        Index("idx_pots_invite_code", "invite_code"),
        Index("idx_pots_creator", "creator_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    match_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("matches.id"))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    stake_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    prediction_type: Mapped[str] = mapped_column(Text, nullable=False)
    max_participants: Mapped[int | None] = mapped_column(Integer)
    deadline: Mapped[datetime | None] = mapped_column(DateTime)
    creator_fee_percent: Mapped[Decimal] = mapped_column(Numeric, default=Decimal("0"))
    status: Mapped[str] = mapped_column(Text, default="open")
    invite_code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    creator = relationship("User", back_populates="pots_created")
    match = relationship("Match", back_populates="pots")
    participants = relationship("Participant", back_populates="pot", cascade="all, delete-orphan")


class Participant(Base):
    __tablename__ = "participants"
    __table_args__ = (
        UniqueConstraint("pot_id", "user_id"),
        Index("idx_participants_pot", "pot_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pots.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    prediction: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="pending")
    virtual_account_number: Mapped[str | None] = mapped_column(Text)
    virtual_account_reference: Mapped[str | None] = mapped_column(Text)
    paid_amount: Mapped[int] = mapped_column(Integer, default=0)
    joined_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    pot = relationship("Pot", back_populates="participants")
    user = relationship("User", back_populates="participations")
    payments = relationship("Payment", back_populates="participant", cascade="all, delete-orphan")
    payouts = relationship("Payout", back_populates="participant", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    participant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("participants.id", ondelete="CASCADE")
    )
    transaction_ref: Mapped[str | None] = mapped_column(Text, unique=True)
    amount: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str | None] = mapped_column(Text)
    webhook_payload: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    participant = relationship("Participant", back_populates="payments")


class Payout(Base):
    __tablename__ = "payouts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    participant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("participants.id", ondelete="CASCADE")
    )
    amount: Mapped[int | None] = mapped_column(Integer)
    bank_account_number: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="pending")
    transaction_ref: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    participant = relationship("Participant", back_populates="payouts")
