# MatchVault — Build Phase Tracker

> **Share this file weekly with your team.** Update the *Current Week* section every Monday (or your sprint start), and move completed items into the changelog at the bottom.

---

## Project at a Glance

| | |
|---|---|
| **Product** | MatchVault MVP |
| **Tagline** | Seamless group match pots with instant payments and automatic settlements |
| **Stack** | Next.js 14 · FastAPI · PostgreSQL · Nomba APIs |
| **Repo** | `/Users/c/matchvault` (update with GitHub URL once pushed) |
| **Stage** | First Building Stage |
| **Last updated** | June 30, 2026 |

---

## Current Week — Week 1 (Jun 30 – Jul 6, 2026)

### 🎯 Weekly Goal
Stand up the full project scaffold and prove the core pot lifecycle locally: **register → create pot → join → generate VA → webhook payment → dashboard**.

### ✅ Completed This Week
- [x] Project repository initialized with monorepo structure (`backend/`, `frontend/`, `docs/`)
- [x] PostgreSQL schema implemented (users, matches, pots, participants, payments, payouts)
- [x] FastAPI backend with all PRD endpoints scaffolded and wired
- [x] JWT auth (register / login)
- [x] Pot creation with invite link generation
- [x] Join pot + prediction selection flow
- [x] Nomba Virtual Account generation (stub — ready for live API key)
- [x] Nomba webhook handler with HMAC signature verification
- [x] Settlement logic (winner calculation + payout records)
- [x] Next.js 14 frontend: landing, auth, dashboard, create pot, join/pay pages
- [x] Docker Compose for local dev (Postgres + backend + frontend)
- [x] Seed data: 3 upcoming FIFA-style matches for testing

### 🔄 In Progress
- [ ] Push repository to GitHub (public)
- [ ] Connect live Nomba Virtual Account API (sandbox credentials)
- [ ] Connect API-Football for real match data

### 📋 Next Week (Week 2)
- [ ] Nomba Bank Transfer integration for winner payouts
- [ ] Real-time dashboard updates (webhook → UI refresh)
- [ ] QR code display for Virtual Account payments
- [ ] Mobile UX polish and error states
- [ ] Deploy backend (Railway) + frontend (Vercel)
- [ ] End-to-end demo video for hackathon judges

### 🚧 Blockers & Risks
| Blocker | Owner | Status |
|---------|-------|--------|
| Nomba sandbox API credentials | — | Waiting |
| API-Football API key | — | Waiting |

---

## Build Phase Overview

```
Phase 1 — Foundation     ██████████ 100%   ← YOU ARE HERE (Week 1 complete)
Phase 2 — Integrations   ██░░░░░░░░  20%
Phase 3 — Polish & Deploy ░░░░░░░░░░   0%
Phase 4 — Demo Ready     ░░░░░░░░░░   0%
```

### Phase 1 — Foundation (Week 1) ✅
| Milestone | Status |
|-----------|--------|
| PRD finalized | ✅ Done |
| Database schema + migrations | ✅ Done |
| FastAPI project + all routes | ✅ Done |
| Next.js frontend scaffold | ✅ Done |
| Docker local dev environment | ✅ Done |
| Auth flow (register/login) | ✅ Done |

### Phase 2 — Integrations (Week 2–3)
| Milestone | Status |
|-----------|--------|
| Nomba Virtual Account (live) | 🔲 Stub only |
| Nomba webhook (live) | 🔲 Handler ready, needs credentials |
| Nomba Bank Transfer payouts | 🔲 Not started |
| API-Football match sync | 🔲 Seed data only |
| Settlement end-to-end test | 🔲 Logic done, needs live data |

### Phase 3 — Polish & Deploy (Week 3–4)
| Milestone | Status |
|-----------|--------|
| Mobile-first UI polish | 🔲 Basic styling done |
| Error handling & loading states | 🔲 Partial |
| Deploy backend (Railway/Vercel) | 🔲 Not started |
| Deploy frontend (Vercel) | 🔲 Not started |
| Environment secrets configured | 🔲 `.env.example` provided |

### Phase 4 — Demo Ready (Week 4)
| Milestone | Status |
|-----------|--------|
| Full demo script (create → pay → settle) | 🔲 Not started |
| Hackathon submission form filled | 🔲 Not started |
| Documentation & README complete | ✅ Done |

---

## API Endpoints — Implementation Status

| Endpoint | Status | Notes |
|----------|--------|-------|
| `POST /auth/register` | ✅ | |
| `POST /auth/login` | ✅ | JWT bearer token |
| `GET /matches/upcoming` | ✅ | Seed data |
| `GET /matches/{id}` | ✅ | |
| `POST /pots` | ✅ | Returns invite link |
| `GET /pots/{invite_code}` | ✅ | Public pot view |
| `GET /pots/my` | ✅ | |
| `POST /pots/{invite_code}/join` | ✅ | |
| `POST /pots/{participant_id}/generate-va` | ✅ | Stub VA |
| `POST /webhooks/nomba` | ✅ | Signature verify ready |
| `POST /pots/{pot_id}/settle` | ✅ | |
| `GET /dashboard` | ✅ | |
| `GET /pots/{pot_id}/details` | ✅ | |

---

## How to Run Locally

```bash
# From project root
cp backend/.env.example backend/.env
docker compose up --build

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API docs: http://localhost:8000/docs
```

---

## Weekly Update Template

_Copy this block each week and fill it in at the top of the file._

```markdown
## Current Week — Week N (Date – Date)

### 🎯 Weekly Goal
[One sentence goal]

### ✅ Completed This Week
- [ ] Item

### 🔄 In Progress
- [ ] Item

### 📋 Next Week
- [ ] Item

### 🚧 Blockers
| Blocker | Owner | Status |
|---------|-------|--------|
| | | |
```

---

## Changelog

### Week 1 — Jun 30, 2026
- Initial project scaffold from PRD v1.0
- Full backend API implemented with PostgreSQL
- Frontend pages: home, login, register, dashboard, create pot, join/pay
- Docker Compose dev environment
- BUILD_PHASE.md created for weekly team updates

---

*Maintained by: Solo Full-Stack + Cloud Developer*
