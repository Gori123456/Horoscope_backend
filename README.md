# Deterministic Horoscope & Predictive Engine - Backend

A high-precision, canonical Vedic (Jyotish) astrological calculation and predictive inference engine built with **Python**, **FastAPI**, and **PostgreSQL**.

---

## 🌟 Key Features

1. **High-Precision Ephemeris Engine:**
   * Julian Day Number (JD) and Local Sidereal Time (LST) to astronomical precision.
   * Chitra Paksha / Lahiri Ayanamsha (precession of the equinoxes) calculation.
   * True Geocentric Ecliptic longitudes for Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu.
   * Automatic Swiss Ephemeris (`pyswisseph`) hardware acceleration when installed, with seamless pure-Python fallback.

2. **Structural Vedic Calculations:**
   * **D1 (Rashi Chart):** 12 Bhavas (Whole Sign System), House cusps, and house lords.
   * **D9 (Navamsha Chart):** Core dharma and relationship divisional chart ($3^\circ 20'$ segments).
   * **Nakshatras & Padas:** 27 lunar mansions and 108 quarters with ruling deities and ganas.
   * **Dignity & Combustion Matrix:** Exalted, Moolatrikona, Own Sign, Friendly, Neutral, Enemy, Debilitated, and solar combustion.

3. **120-Year Vimshottari Dasha Engine:**
   * Exact starting balance from Moon's nakshatra longitude at birth.
   * Nested Mahadashas (major periods) and Antardashas (sub-periods) calculated with day-level accuracy.
   * Active Dasha identification for any historical, current, or future timestamp.

4. **Canonical Yogas & Doshas Rule Engine:**
   * 20+ classical combinations including *Gajakesari*, *Budhaditya*, *Pancha Mahapurusha* (*Ruchaka*, *Bhadra*, *Hamsa*, *Malavya*, *Shasha*), *Dharma-Karmadhipati Raja Yogas*, *Maha Dhana Yogas*, *Viparita Raja Yogas*, *Mangal Dosha* (with cancellations), *Kemadruma Dosha*, and *Kaal Sarp Yoga*.

5. **Quantitative Domain Scoring & Explainable Predictions:**
   * 0–100 ratings across 6 life pillars: **Career**, **Wealth**, **Health**, **Relationships**, **Intellect**, and **Spirituality**.
   * Transparent readings linking back to exact planetary placements and active dasha lords.

6. **Real-Time Transits (Gochar):**
   * Saturn *Sade Sati* (Phase 1, 2, 3), *Kantaka Shani*, and *Ashtama Shani*.
   * Jupiter *Guru Gochar* benefic transit windows.

---

## 🚀 Getting Started

### 1. Requirements
* Python 3.10+
* (Optional) PostgreSQL 14+ (Local SQLite fallback is active out of the box)

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Database
By default, the backend runs seamlessly on local storage (`horoscope.db`).
To connect your production PostgreSQL database:
Set the environment variable:
```bash
# Windows PowerShell
$env:DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/horoscope_db"

# Linux / MacOS
export DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/horoscope_db"
```
Execute the DDL schema in PostgreSQL:
```bash
psql -U postgres -d horoscope_db -f app/db/schema.sql
```

### 4. Run the API Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger Documentation will be available at:
`http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/horoscope/calculate` | Computes full D1, D9, nakshatras, houses, dashas, and saves record. |
| `GET` | `/api/horoscope/{chart_id}` | Retrieves chart details by ID. |
| `GET` | `/api/horoscope/{chart_id}/dasha` | Retrieves 120-year Vimshottari timeline and active period. |
| `GET` | `/api/horoscope/{chart_id}/yogas` | Retrieves all detected yogas and doshas. |
| `GET` | `/api/horoscope/{chart_id}/predictions` | Retrieves domain scores (0-100) and structured readings. |
| `GET` | `/api/horoscope/{chart_id}/transits` | Computes current transits and Sade Sati status. |
| `GET` | `/api/health` | Health check endpoint. |

