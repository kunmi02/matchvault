"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("external_id", sa.Integer(), nullable=True),
        sa.Column("home_team", sa.Text(), nullable=True),
        sa.Column("away_team", sa.Text(), nullable=True),
        sa.Column("match_date", sa.DateTime(), nullable=True),
        sa.Column("status", sa.Text(), server_default="upcoming", nullable=True),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_id"),
    )
    op.create_table(
        "pots",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("creator_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("match_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("stake_amount", sa.Integer(), nullable=False),
        sa.Column("prediction_type", sa.Text(), nullable=False),
        sa.Column("max_participants", sa.Integer(), nullable=True),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("creator_fee_percent", sa.Numeric(), server_default="0", nullable=True),
        sa.Column("status", sa.Text(), server_default="open", nullable=True),
        sa.Column("invite_code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invite_code"),
    )
    op.create_table(
        "participants",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("pot_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("prediction", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), server_default="pending", nullable=True),
        sa.Column("virtual_account_number", sa.Text(), nullable=True),
        sa.Column("virtual_account_reference", sa.Text(), nullable=True),
        sa.Column("paid_amount", sa.Integer(), server_default="0", nullable=True),
        sa.Column("joined_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(["pot_id"], ["pots.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pot_id", "user_id"),
    )
    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("participant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("transaction_ref", sa.Text(), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=True),
        sa.Column("status", sa.Text(), nullable=True),
        sa.Column("webhook_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(["participant_id"], ["participants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("transaction_ref"),
    )
    op.create_table(
        "payouts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("participant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=True),
        sa.Column("bank_account_number", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), server_default="pending", nullable=True),
        sa.Column("transaction_ref", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=True),
        sa.ForeignKeyConstraint(["participant_id"], ["participants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("idx_pots_invite_code", "pots", ["invite_code"], unique=False)
    op.create_index("idx_pots_creator", "pots", ["creator_id"], unique=False)
    op.create_index("idx_participants_pot", "participants", ["pot_id"], unique=False)
    op.create_index("idx_matches_status", "matches", ["status"], unique=False)

    op.execute(
        """
        INSERT INTO matches (external_id, home_team, away_team, match_date, status) VALUES
            (1001, 'Nigeria', 'Argentina', NOW() + INTERVAL '3 days', 'upcoming'),
            (1002, 'Brazil', 'France', NOW() + INTERVAL '5 days', 'upcoming'),
            (1003, 'Germany', 'Spain', NOW() + INTERVAL '7 days', 'upcoming')
        """
    )


def downgrade() -> None:
    op.drop_index("idx_matches_status", table_name="matches")
    op.drop_index("idx_participants_pot", table_name="participants")
    op.drop_index("idx_pots_creator", table_name="pots")
    op.drop_index("idx_pots_invite_code", table_name="pots")
    op.drop_table("payouts")
    op.drop_table("payments")
    op.drop_table("participants")
    op.drop_table("pots")
    op.drop_table("matches")
    op.drop_table("users")
