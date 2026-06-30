-- Legacy reference schema. Use Alembic for migrations:
--   cd backend && alembic upgrade head

-- MatchVault MVP schema (PRD v1.0)

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    external_id INTEGER UNIQUE,
    home_team TEXT,
    away_team TEXT,
    match_date TIMESTAMP,
    status TEXT DEFAULT 'upcoming',
    result JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE pots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    creator_id UUID REFERENCES users(id),
    match_id INTEGER REFERENCES matches(id),
    name TEXT NOT NULL,
    description TEXT,
    stake_amount INTEGER NOT NULL,
    prediction_type TEXT NOT NULL,
    max_participants INTEGER,
    deadline TIMESTAMP,
    creator_fee_percent DECIMAL DEFAULT 0,
    status TEXT DEFAULT 'open',
    invite_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pot_id UUID REFERENCES pots(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    prediction TEXT,
    status TEXT DEFAULT 'pending',
    virtual_account_number TEXT,
    virtual_account_reference TEXT,
    paid_amount INTEGER DEFAULT 0,
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (pot_id, user_id)
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    participant_id UUID REFERENCES participants(id) ON DELETE CASCADE,
    transaction_ref TEXT UNIQUE,
    amount INTEGER,
    status TEXT,
    webhook_payload JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE payouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    participant_id UUID REFERENCES participants(id) ON DELETE CASCADE,
    amount INTEGER,
    bank_account_number TEXT,
    status TEXT DEFAULT 'pending',
    transaction_ref TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pots_invite_code ON pots(invite_code);
CREATE INDEX idx_pots_creator ON pots(creator_id);
CREATE INDEX idx_participants_pot ON participants(pot_id);
CREATE INDEX idx_matches_status ON matches(status);

-- Seed sample upcoming matches for local dev
INSERT INTO matches (external_id, home_team, away_team, match_date, status) VALUES
    (1001, 'Nigeria', 'Argentina', NOW() + INTERVAL '3 days', 'upcoming'),
    (1002, 'Brazil', 'France', NOW() + INTERVAL '5 days', 'upcoming'),
    (1003, 'Germany', 'Spain', NOW() + INTERVAL '7 days', 'upcoming');
