# MatchVault MVP - Product Requirements Document (PRD)

**Product Name**: MatchVault  
**Version**: 1.0 (Hackathon MVP)  
**Date**: June 2026  
**Author**: Solo Full-Stack + Cloud Developer

## 1. Product Overview

**Tagline**: Seamless group match pots with instant payments and automatic settlements.

**Vision**:  
MatchVault enables friends, fans, office groups, and communities to create, join, and settle FIFA (and other sports) prediction pots transparently using Nomba's payment infrastructure.

**Core Value Proposition**:  
Eliminate manual collection, disputes, and delayed settlements in group pools by using Nomba Virtual Accounts for collections and Bank Transfers for payouts, with real-time webhook updates.

## 2. Objectives & Success Criteria
- Strong demonstration of Nomba APIs (Virtual Accounts, Webhooks, Bank Transfers).
- Fun, timely product around 2026 FIFA World Cup.
- End-to-end functional MVP by end of build sprint.

## 3. Target Users
- Pot Creators (organizers)
- Participants (friends, colleagues, diaspora fans)

## 4. Key Features & Use Cases

### 4.1 Authentication
- Email/password or magic link (Supabase Auth)

### 4.2 Pot Creation
- Browse upcoming matches (API-Football)
- Select prediction type (Winner, Over/Under)
- Set stake, rules, creator fee
- Generate invite link

### 4.3 Joining a Pot
- Click invite link
- Choose prediction
- Pay via dynamic Nomba Virtual Account + QR
- Fallback: Checkout

### 4.4 Real-time Dashboard
- Live progress via webhooks
- Participant status

### 4.5 Settlement & Payouts
- Trigger settlement after match
- Fetch result from sports API
- Calculate winners
- Disburse via Nomba Bank Transfer API

## 5. Database Schema (PostgreSQL)

See `backend/migrations/init.sql` for the live schema.

Tables: `users`, `matches`, `pots`, `participants`, `payments`, `payouts`

## 6. API Endpoints (FastAPI)

### Auth & Users
- `POST /auth/login`
- `POST /auth/register`

### Matches
- `GET /matches/upcoming`
- `GET /matches/{match_id}`

### Pots
- `POST /pots` → Create pot (returns invite link)
- `GET /pots/{invite_code}` → Public pot details
- `GET /pots/my` → User's created & joined pots

### Join & Payment
- `POST /pots/{invite_code}/join` → Choose prediction
- `POST /pots/{participant_id}/generate-va` → Create Nomba Virtual Account

### Webhooks
- `POST /webhooks/nomba` → Handle Nomba payment webhooks (signature verification)

### Settlement
- `POST /pots/{pot_id}/settle` → Trigger settlement & payouts

### Admin / Dashboard
- `GET /dashboard`
- `GET /pots/{pot_id}/details`

## 7. Technical Stack
- Frontend: Next.js 14 + Tailwind (Vercel)
- Backend: Python + FastAPI (Railway/Vercel)
- Database: PostgreSQL (Neon/Supabase)
- Others: Docker for local dev, API-Football, Nomba APIs

## 8. Non-Functional
- Secure webhook verification
- Idempotency & retry logic
- Mobile-first UX
