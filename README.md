# MatchVault

**Seamless group match pots with instant payments and automatic settlements.**

MatchVault lets friends, fans, and communities create FIFA prediction pots, collect stakes via Nomba Virtual Accounts, and automatically settle winners through Bank Transfers.

## Quick Start

```bash
git clone <your-repo-url>
cd matchvault

cp backend/.env.example backend/.env
# Add your Nomba and API-Football keys to backend/.env

docker compose up --build
# Backend runs `alembic upgrade head` on startup
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

## Local Development (without Docker)

**Prerequisites:** Python 3.12, Node.js 18+, PostgreSQL 16

> Use Python **3.12** locally — 3.14 is not yet supported by Pydantic's native deps. On macOS: `brew install python@3.12`

Copy env files and add your API keys (if you have not already):

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

### Database

Run PostgreSQL locally, or start only the database container:

```bash
docker compose up db -d
```

From `backend/` with your venv activated, run migrations:

```bash
alembic upgrade head
```

Useful Alembic commands:

```bash
alembic current          # show applied revision
alembic history          # list all revisions
alembic downgrade -1     # roll back one revision
```

For a local Postgres install, create the database first:

```bash
createdb matchvault
alembic upgrade head
```


### Backend

```bash
cd backend
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API runs at http://localhost:8000 (docs at http://localhost:8000/docs).

### Frontend

In a separate terminal:

```bash
cd frontend
npm install
cp .env.example .env.local   # if you have not already
npm run dev
```

Frontend runs at http://localhost:3000.

## Project Structure

```
matchvault/
├── BUILD_PHASE.md      # Weekly build status (share with team)
├── docker-compose.yml
├── docs/
│   └── PRD.md          # Product requirements
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   └── alembic/        # Database migrations (Alembic)
└── frontend/
    └── src/app/        # Next.js 14 pages
```

## Core Flow

1. **Register / Login** — JWT auth
2. **Create Pot** — Pick a match, set stake & rules, get invite link
3. **Join Pot** — Choose prediction, generate Nomba Virtual Account
4. **Pay** — Transfer to VA; webhook marks participant as paid
5. **Settle** — Creator triggers settlement; winners get payout records

## Environment Variables

**Backend** — see `backend/.env.example`:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key |
| `NOMBA_API_KEY` | Nomba API credentials |
| `NOMBA_WEBHOOK_SECRET` | Webhook HMAC secret |
| `API_FOOTBALL_KEY` | API-Football for live match data |
| `FRONTEND_URL` | Used for invite link generation |

**Frontend** — see `frontend/.env.example` (copy to `.env.local`):

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL (default: `http://localhost:8000`) |

## Weekly Updates

See **[BUILD_PHASE.md](./BUILD_PHASE.md)** for the current build phase, completed milestones, blockers, and weekly update template.

## Hackathon Submission

- **One-line summary:** Group FIFA prediction pots with Nomba instant payments and auto-settlement
- **Repo:** [add GitHub URL]
- **Docs:** [BUILD_PHASE.md](./BUILD_PHASE.md) · [docs/PRD.md](./docs/PRD.md)

## License

MIT
