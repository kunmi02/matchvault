from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, dashboard, matches, pots, webhooks

app = FastAPI(
    title="MatchVault API",
    description="Group match prediction pots with Nomba payments",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(pots.router)
app.include_router(webhooks.router)
app.include_router(dashboard.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "matchvault-api"}
