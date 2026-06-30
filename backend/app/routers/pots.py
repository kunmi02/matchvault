from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Participant
from app.routers.auth import get_current_user
from app.models import User
from app.schemas import (
    JoinPotRequest,
    ParticipantResponse,
    PotCreate,
    PotDetailsResponse,
    PotResponse,
    SettlementResponse,
    VirtualAccountResponse,
)
from app.services import (
    create_pot,
    generate_virtual_account,
    get_match,
    get_pot_by_id,
    get_pot_by_invite,
    get_user_pots,
    join_pot,
    pot_to_response,
    settle_pot,
)
from sqlalchemy import select

router = APIRouter(prefix="/pots", tags=["pots"])


@router.post("", response_model=PotResponse, status_code=201)
async def create_new_pot(
    data: PotCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    match = await get_match(db, data.match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    pot = await create_pot(db, user.id, data)
    pot.match = match
    pot.participants = []
    return pot_to_response(pot)


@router.get("/my", response_model=list[PotResponse])
async def my_pots(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    pots = await get_user_pots(db, user.id)
    return [pot_to_response(p) for p in pots]


@router.get("/{invite_code}", response_model=PotDetailsResponse)
async def public_pot_details(invite_code: str, db: AsyncSession = Depends(get_db)):
    pot = await get_pot_by_invite(db, invite_code)
    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")
    base = pot_to_response(pot)
    return PotDetailsResponse(
        **base.model_dump(),
        participants=[ParticipantResponse.model_validate(p) for p in pot.participants],
    )


@router.post("/{invite_code}/join", response_model=ParticipantResponse, status_code=201)
async def join_pot_endpoint(
    invite_code: str,
    data: JoinPotRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pot = await get_pot_by_invite(db, invite_code)
    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")
    if pot.status != "open":
        raise HTTPException(status_code=400, detail="Pot is not open")
    if pot.max_participants and len(pot.participants) >= pot.max_participants:
        raise HTTPException(status_code=400, detail="Pot is full")
    existing = await db.execute(
        select(Participant).where(Participant.pot_id == pot.id, Participant.user_id == user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Already joined this pot")
    participant = await join_pot(db, pot, user.id, data.prediction)
    return participant


@router.post("/{participant_id}/generate-va", response_model=VirtualAccountResponse)
async def generate_va(
    participant_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(select(Participant).where(Participant.id == participant_id))
    participant = result.scalar_one_or_none()
    if not participant or participant.user_id != user.id:
        raise HTTPException(status_code=404, detail="Participant not found")
    pot = await get_pot_by_id(db, participant.pot_id)
    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")
    participant = await generate_virtual_account(db, participant, pot)
    return VirtualAccountResponse(
        participant_id=participant.id,
        virtual_account_number=participant.virtual_account_number or "",
        virtual_account_reference=participant.virtual_account_reference or "",
        amount=pot.stake_amount,
        qr_code_url=None,
    )


@router.get("/{pot_id}/details", response_model=PotDetailsResponse)
async def pot_details(
    pot_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pot = await get_pot_by_id(db, pot_id)
    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")
    base = pot_to_response(pot)
    return PotDetailsResponse(
        **base.model_dump(),
        participants=[ParticipantResponse.model_validate(p) for p in pot.participants],
    )


@router.post("/{pot_id}/settle", response_model=SettlementResponse)
async def settle_pot_endpoint(
    pot_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    pot = await get_pot_by_id(db, pot_id)
    if not pot:
        raise HTTPException(status_code=404, detail="Pot not found")
    if pot.creator_id != user.id:
        raise HTTPException(status_code=403, detail="Only the creator can settle")
    try:
        winners, payout_count = await settle_pot(db, pot)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SettlementResponse(
        pot_id=pot.id,
        status="settled",
        winners=winners,
        payouts_initiated=payout_count,
    )
