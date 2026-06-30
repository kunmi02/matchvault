from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import MatchResponse
from app.services import get_match, get_upcoming_matches

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/upcoming", response_model=list[MatchResponse])
async def upcoming_matches(db: AsyncSession = Depends(get_db)):
    return await get_upcoming_matches(db)


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match_by_id(match_id: int, db: AsyncSession = Depends(get_db)):
    match = await get_match(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match
