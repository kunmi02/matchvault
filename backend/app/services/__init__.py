import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models import Match, Participant, Payment, Payout, Pot, User
from app.schemas import PotCreate, PotResponse, UserRegister

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> uuid.UUID:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return uuid.UUID(payload["sub"])


def generate_invite_code() -> str:
    return secrets.token_urlsafe(8)


def build_invite_link(invite_code: str) -> str:
    return f"{settings.frontend_url}/pots/{invite_code}"


async def register_user(db: AsyncSession, data: UserRegister) -> User:
    user = User(email=data.email, name=data.name, password_hash=hash_password(data.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.password_hash or not verify_password(password, user.password_hash):
        return None
    return user


async def get_upcoming_matches(db: AsyncSession) -> list[Match]:
    result = await db.execute(
        select(Match).where(Match.status == "upcoming").order_by(Match.match_date.asc())
    )
    return list(result.scalars().all())


async def get_match(db: AsyncSession, match_id: int) -> Match | None:
    result = await db.execute(select(Match).where(Match.id == match_id))
    return result.scalar_one_or_none()


async def create_pot(db: AsyncSession, creator_id: uuid.UUID, data: PotCreate) -> Pot:
    pot = Pot(
        creator_id=creator_id,
        match_id=data.match_id,
        name=data.name,
        description=data.description,
        stake_amount=data.stake_amount,
        prediction_type=data.prediction_type,
        max_participants=data.max_participants,
        deadline=data.deadline,
        creator_fee_percent=data.creator_fee_percent,
        invite_code=generate_invite_code(),
    )
    db.add(pot)
    await db.commit()
    await db.refresh(pot)
    return pot


async def get_pot_by_invite(db: AsyncSession, invite_code: str) -> Pot | None:
    result = await db.execute(
        select(Pot)
        .options(selectinload(Pot.match), selectinload(Pot.participants))
        .where(Pot.invite_code == invite_code)
    )
    return result.scalar_one_or_none()


async def get_pot_by_id(db: AsyncSession, pot_id: uuid.UUID) -> Pot | None:
    result = await db.execute(
        select(Pot)
        .options(selectinload(Pot.match), selectinload(Pot.participants))
        .where(Pot.id == pot_id)
    )
    return result.scalar_one_or_none()


async def get_user_pots(db: AsyncSession, user_id: uuid.UUID) -> list[Pot]:
    created = await db.execute(
        select(Pot)
        .options(selectinload(Pot.match), selectinload(Pot.participants))
        .where(Pot.creator_id == user_id)
    )
    joined = await db.execute(
        select(Pot)
        .join(Participant)
        .options(selectinload(Pot.match), selectinload(Pot.participants))
        .where(Participant.user_id == user_id)
    )
    pots = {p.id: p for p in created.scalars().all()}
    for pot in joined.scalars().all():
        pots[pot.id] = pot
    return list(pots.values())


def pot_to_response(pot: Pot) -> PotResponse:
    return PotResponse(
        id=pot.id,
        name=pot.name,
        description=pot.description,
        stake_amount=pot.stake_amount,
        prediction_type=pot.prediction_type,
        max_participants=pot.max_participants,
        deadline=pot.deadline,
        creator_fee_percent=pot.creator_fee_percent,
        status=pot.status,
        invite_code=pot.invite_code,
        invite_link=build_invite_link(pot.invite_code),
        match=pot.match,
        participant_count=len(pot.participants),
    )


async def join_pot(db: AsyncSession, pot: Pot, user_id: uuid.UUID, prediction: str) -> Participant:
    participant = Participant(pot_id=pot.id, user_id=user_id, prediction=prediction)
    db.add(participant)
    await db.commit()
    await db.refresh(participant)
    return participant


async def generate_virtual_account(db: AsyncSession, participant: Participant, pot: Pot) -> Participant:
    """Create a Nomba Virtual Account (stub — wire to Nomba API in production)."""
    reference = f"MV-{participant.id.hex[:12].upper()}"
    account_number = f"9{secrets.randbelow(10_000_000_000):010d}"
    participant.virtual_account_number = account_number
    participant.virtual_account_reference = reference
    await db.commit()
    await db.refresh(participant)
    return participant


def verify_nomba_signature(payload: bytes, signature: str) -> bool:
    if not settings.nomba_webhook_secret:
        return True
    expected = hmac.new(
        settings.nomba_webhook_secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


async def process_nomba_webhook(db: AsyncSession, payload: dict) -> Payment | None:
    ref = payload.get("reference") or payload.get("transaction_ref")
    if not ref:
        return None

    result = await db.execute(select(Participant).where(Participant.virtual_account_reference == ref))
    participant = result.scalar_one_or_none()
    if not participant:
        return None

    existing = await db.execute(select(Payment).where(Payment.transaction_ref == ref))
    if existing.scalar_one_or_none():
        return None

    amount = int(payload.get("amount", 0))
    payment = Payment(
        participant_id=participant.id,
        transaction_ref=ref,
        amount=amount,
        status="success",
        webhook_payload=payload,
    )
    participant.paid_amount = amount
    participant.status = "paid"
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def settle_pot(db: AsyncSession, pot: Pot) -> tuple[list[uuid.UUID], int]:
    if not pot.match or not pot.match.result:
        raise ValueError("Match result not available")

    result = pot.match.result
    home_score = result.get("home_score", 0)
    away_score = result.get("away_score", 0)

    winners: list[Participant] = []
    for p in pot.participants:
        if p.status != "paid":
            p.status = "lost"
            continue
        won = False
        if pot.prediction_type == "winner":
            if p.prediction == "home" and home_score > away_score:
                won = True
            elif p.prediction == "away" and away_score > home_score:
                won = True
            elif p.prediction == "draw" and home_score == away_score:
                won = True
        elif pot.prediction_type == "over_under":
            total = home_score + away_score
            line = result.get("line", 2.5)
            if p.prediction == "over" and total > line:
                won = True
            elif p.prediction == "under" and total < line:
                won = True
        p.status = "won" if won else "lost"
        if won:
            winners.append(p)

    pot.status = "settled"
    payout_count = 0
    if winners:
        pool = sum(p.paid_amount for p in pot.participants if p.status in ("won", "lost", "paid"))
        fee = int(pool * float(pot.creator_fee_percent) / 100)
        prize_pool = pool - fee
        share = prize_pool // len(winners)
        for winner in winners:
            payout = Payout(
                participant_id=winner.id,
                amount=share,
                status="pending",
                transaction_ref=f"PAYOUT-{winner.id.hex[:12].upper()}",
            )
            db.add(payout)
            payout_count += 1

    await db.commit()
    return [w.id for w in winners], payout_count


async def get_dashboard(db: AsyncSession, user_id: uuid.UUID) -> dict:
    created_count = await db.execute(select(func.count()).select_from(Pot).where(Pot.creator_id == user_id))
    joined_count = await db.execute(
        select(func.count()).select_from(Participant).where(Participant.user_id == user_id)
    )
    staked = await db.execute(
        select(func.coalesce(func.sum(Participant.paid_amount), 0)).where(Participant.user_id == user_id)
    )
    open_pots = await db.execute(
        select(func.count()).select_from(Pot).where(Pot.creator_id == user_id, Pot.status == "open")
    )
    recent = await get_user_pots(db, user_id)
    recent.sort(key=lambda p: p.created_at, reverse=True)
    return {
        "pots_created": created_count.scalar() or 0,
        "pots_joined": joined_count.scalar() or 0,
        "total_staked": int(staked.scalar() or 0),
        "open_pots": open_pots.scalar() or 0,
        "recent_pots": [pot_to_response(p) for p in recent[:5]],
    }
