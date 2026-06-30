from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services import process_nomba_webhook, verify_nomba_signature

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/nomba")
async def nomba_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_nomba_signature: str | None = Header(default=None),
):
    body = await request.body()
    if x_nomba_signature and not verify_nomba_signature(body, x_nomba_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()
    payment = await process_nomba_webhook(db, payload)
    if not payment:
        return {"status": "ignored"}
    return {"status": "processed", "payment_id": str(payment.id)}
