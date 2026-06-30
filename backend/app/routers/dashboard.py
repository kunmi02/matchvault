from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.routers.auth import get_current_user
from app.models import User
from app.schemas import DashboardResponse
from app.services import get_dashboard

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    data = await get_dashboard(db, user.id)
    return DashboardResponse(**data)
