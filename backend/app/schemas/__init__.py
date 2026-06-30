from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str | None

    model_config = {"from_attributes": True}


class MatchResponse(BaseModel):
    id: int
    external_id: int | None
    home_team: str | None
    away_team: str | None
    match_date: datetime | None
    status: str
    result: dict | None = None

    model_config = {"from_attributes": True}


class PotCreate(BaseModel):
    match_id: int
    name: str
    description: str | None = None
    stake_amount: int = Field(gt=0)
    prediction_type: str = Field(pattern="^(winner|over_under)$")
    max_participants: int | None = Field(default=None, gt=0)
    deadline: datetime | None = None
    creator_fee_percent: Decimal = Field(default=Decimal("0"), ge=0, le=100)


class PotResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    stake_amount: int
    prediction_type: str
    max_participants: int | None
    deadline: datetime | None
    creator_fee_percent: Decimal
    status: str
    invite_code: str
    invite_link: str | None = None
    match: MatchResponse | None = None
    participant_count: int = 0

    model_config = {"from_attributes": True}


class JoinPotRequest(BaseModel):
    prediction: str


class ParticipantResponse(BaseModel):
    id: UUID
    prediction: str | None
    status: str
    paid_amount: int
    virtual_account_number: str | None = None

    model_config = {"from_attributes": True}


class VirtualAccountResponse(BaseModel):
    participant_id: UUID
    virtual_account_number: str
    virtual_account_reference: str
    amount: int
    qr_code_url: str | None = None


class PotDetailsResponse(PotResponse):
    participants: list[ParticipantResponse] = []


class DashboardResponse(BaseModel):
    pots_created: int
    pots_joined: int
    total_staked: int
    open_pots: int
    recent_pots: list[PotResponse]


class SettlementResponse(BaseModel):
    pot_id: UUID
    status: str
    winners: list[UUID]
    payouts_initiated: int
