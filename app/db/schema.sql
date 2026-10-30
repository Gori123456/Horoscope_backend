-- ======================================================================
-- PostgreSQL Relational Schema for Deterministic Horoscope Platform
-- Compatible with PostgreSQL 14, 15, 16, 17, 18+
-- ======================================================================

-- 1. Create Extension for UUID generation if not present
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Users / Subject Birth Records Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    birth_date DATE NOT NULL,
    birth_time TIME NOT NULL,
    birth_timezone VARCHAR(60) NOT NULL DEFAULT 'UTC',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    place_name VARCHAR(200),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Natal Charts (D1 Rashi & D9 Navamsha) Table
CREATE TABLE IF NOT EXISTS natal_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    julian_day DOUBLE PRECISION NOT NULL,
    ayanamsha_val DOUBLE PRECISION NOT NULL,
    ascendant_degree DOUBLE PRECISION NOT NULL,
    ascendant_sign INT NOT NULL,
    chart_data JSONB NOT NULL,    -- 9 Navagrahas: coordinates, nakshatras, dignities
    houses_data JSONB NOT NULL,   -- 12 Bhavas: cusps, lords, classifications
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast user chart lookups
CREATE INDEX IF NOT EXISTS idx_natal_charts_user_id ON natal_charts(user_id);

-- 4. Vimshottari Dasha Records Table
CREATE TABLE IF NOT EXISTS dasha_timelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES natal_charts(id) ON DELETE CASCADE,
    level INT NOT NULL,           -- 1 = Mahadasha, 2 = Antardasha
    planet VARCHAR(20) NOT NULL,
    parent_planet VARCHAR(20),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dasha_chart_id ON dasha_timelines(chart_id);
CREATE INDEX IF NOT EXISTS idx_dasha_dates ON dasha_timelines(start_date, end_date);

-- 5. Detected Yogas & Doshas Table
CREATE TABLE IF NOT EXISTS chart_yogas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES natal_charts(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(60) NOT NULL,
    impact_weight INT NOT NULL,
    description TEXT NOT NULL,
    planets_involved JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chart_yogas_chart_id ON chart_yogas(chart_id);

-- 6. Computed Predictive Domain Scores Table
CREATE TABLE IF NOT EXISTS prediction_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES natal_charts(id) ON DELETE CASCADE,
    domain_scores JSONB NOT NULL, -- Career, Wealth, Health, Relationships, Intellect, Spirituality
    readings JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_prediction_scores_chart_id ON prediction_scores(chart_id);

