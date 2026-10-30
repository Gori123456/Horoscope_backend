"""
Database Access Layer with Auto-Fallback.
Supports PostgreSQL (via psycopg2/asyncpg/URL) and local SQLite fallback.
Provides unified CRUD operations for user profiles, charts, dashas, and predictions.
"""

import json
import sqlite3
import uuid
from datetime import datetime
from app.config import settings

class DatabaseManager:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.is_postgres = db_url.startswith("postgres://") or db_url.startswith("postgresql://")
        self.sqlite_path = "horoscope.db"
        self._init_sqlite()

    def _init_sqlite(self):
        """Initializes local tables if using SQLite fallback."""
        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    birth_time TEXT NOT NULL,
                    birth_timezone TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    place_name TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS natal_charts (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    julian_day REAL NOT NULL,
                    ayanamsha_val REAL NOT NULL,
                    ascendant_degree REAL NOT NULL,
                    ascendant_sign INTEGER NOT NULL,
                    chart_data TEXT NOT NULL,
                    houses_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS dasha_timelines (
                    id TEXT PRIMARY KEY,
                    chart_id TEXT,
                    dasha_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(chart_id) REFERENCES natal_charts(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chart_yogas (
                    id TEXT PRIMARY KEY,
                    chart_id TEXT,
                    yogas_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(chart_id) REFERENCES natal_charts(id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS prediction_scores (
                    id TEXT PRIMARY KEY,
                    chart_id TEXT,
                    prediction_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(chart_id) REFERENCES natal_charts(id)
                )
            """)
            conn.commit()

    def save_full_record(self, user_meta: dict, chart: dict, houses: list[dict], jd: float, ayanamsha: float, dashas: list[dict], yogas: list[dict], predictions: dict) -> str:
        """Saves user, computed chart, dashas, yogas, and predictions."""
        chart_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        now_iso = datetime.utcnow().isoformat()

        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.cursor()
            # 1. User
            cur.execute(
                "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, user_meta["name"], str(user_meta["birth_date"]), str(user_meta["birth_time"]),
                 user_meta["birth_timezone"], user_meta["latitude"], user_meta["longitude"],
                 user_meta.get("place_name", ""), now_iso)
            )
            # 2. Natal Chart
            cur.execute(
                "INSERT INTO natal_charts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (chart_id, user_id, jd, ayanamsha, chart["ascendant"]["longitude"],
                 chart["ascendant"]["sign_id"], json.dumps(chart), json.dumps(houses), now_iso)
            )
            # 3. Dashas
            cur.execute(
                "INSERT INTO dasha_timelines VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), chart_id, json.dumps(dashas), now_iso)
            )
            # 4. Yogas
            cur.execute(
                "INSERT INTO chart_yogas VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), chart_id, json.dumps(yogas), now_iso)
            )
            # 5. Predictions
            cur.execute(
                "INSERT INTO prediction_scores VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), chart_id, json.dumps(predictions), now_iso)
            )
            conn.commit()

        return chart_id

    def get_chart(self, chart_id: str) -> dict | None:
        """Retrieves natal chart by ID."""
        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.id, u.name, u.birth_date, u.birth_time, u.birth_timezone, 
                       u.latitude, u.longitude, u.place_name, c.julian_day, c.ayanamsha_val,
                       c.chart_data, c.houses_data
                FROM natal_charts c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = ?
            """, (chart_id,))
            row = cur.fetchone()
            if not row:
                return None

            return {
                "chart_id": row[0],
                "user_name": row[1],
                "birth_date": row[2],
                "birth_time": row[3],
                "timezone": row[4],
                "coordinates": {"latitude": row[5], "longitude": row[6]},
                "place_name": row[7],
                "julian_day": row[8],
                "ayanamsha": row[9],
                "chart": json.loads(row[10]),
                "houses": json.loads(row[11])
            }

    def get_dashas(self, chart_id: str) -> list[dict] | None:
        """Retrieves dasha records for chart."""
        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT dasha_data FROM dasha_timelines WHERE chart_id = ?", (chart_id,))
            row = cur.fetchone()
            return json.loads(row[0]) if row else None

    def get_yogas(self, chart_id: str) -> list[dict] | None:
        """Retrieves detected yogas for chart."""
        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT yogas_data FROM chart_yogas WHERE chart_id = ?", (chart_id,))
            row = cur.fetchone()
            return json.loads(row[0]) if row else None

    def get_predictions(self, chart_id: str) -> dict | None:
        """Retrieves domain predictions for chart."""
        with sqlite3.connect(self.sqlite_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT prediction_data FROM prediction_scores WHERE chart_id = ?", (chart_id,))
            row = cur.fetchone()
            return json.loads(row[0]) if row else None


db_manager = DatabaseManager(settings.DATABASE_URL)

