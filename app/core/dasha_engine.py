"""
Vimshottari Dasha Engine.
Computes the 120-year planetary chronology:
- Balance of Birth Dasha from Moon's Nakshatra
- Full sequence of Mahadashas (major periods)
- Antardashas (sub-periods)
- Active dasha lookup for any point in time.
"""

from datetime import datetime, timedelta
from app.core.constants import DASHA_ORDER, TOTAL_DASHA_YEARS

# Mapping nakshatra lord index to dasha lord
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]


def calculate_vimshottari_dashas(birth_datetime: datetime, moon_nakshatra_info: dict) -> list[dict]:
    """
    Computes complete 120-year Vimshottari Mahadashas and nested Antardashas.
    """
    nak_lord = moon_nakshatra_info["lord"]
    frac_elapsed = moon_nakshatra_info["nakshatra_fraction_elapsed"]
    frac_remaining = 1.0 - frac_elapsed

    # Find starting index in DASHA_ORDER
    start_idx = next(i for i, d in enumerate(DASHA_ORDER) if d["planet"] == nak_lord)
    current_dt = birth_datetime

    mahadashas = []
    days_in_year = 365.2425  # Tropical solar year standard

    # 1. First Mahadasha (partial balance)
    first_dasha_meta = DASHA_ORDER[start_idx]
    remaining_years = first_dasha_meta["years"] * frac_remaining
    end_dt = current_dt + timedelta(days=remaining_years * days_in_year)

    # Calculate Antardashas for first dasha
    # For initial balance, we compute standard antardasha periods and trim those already past
    antardashas_first = _generate_antardashas(first_dasha_meta["planet"], first_dasha_meta["years"], current_dt, end_dt)

    mahadashas.append({
        "level": 1,
        "planet": first_dasha_meta["planet"],
        "total_years": first_dasha_meta["years"],
        "balance_years": round(remaining_years, 3),
        "start_date": current_dt.isoformat(),
        "end_date": end_dt.isoformat(),
        "antardashas": antardashas_first
    })
    current_dt = end_dt

    # 2. Subsequent 8 Mahadashas (full periods)
    for step in range(1, 9):
        idx = (start_idx + step) % 9
        d_meta = DASHA_ORDER[idx]
        d_years = d_meta["years"]
        d_end_dt = current_dt + timedelta(days=d_years * days_in_year)

        antar_list = _generate_antardashas(d_meta["planet"], d_years, current_dt, d_end_dt)

        mahadashas.append({
            "level": 1,
            "planet": d_meta["planet"],
            "total_years": d_years,
            "balance_years": d_years,
            "start_date": current_dt.isoformat(),
            "end_date": d_end_dt.isoformat(),
            "antardashas": antar_list
        })
        current_dt = d_end_dt

    return mahadashas


def _generate_antardashas(maha_planet: str, maha_years: float, maha_start: datetime, maha_end: datetime) -> list[dict]:
    """
    Divides a Mahadasha into 9 Antardashas based on classical proportional rule:
    Antar Duration = (Maha Years * Antar Years) / 120 years.
    """
    days_in_year = 365.2425
    start_idx = next(i for i, d in enumerate(DASHA_ORDER) if d["planet"] == maha_planet)
    antardashas = []
    c_dt = maha_start

    for step in range(9):
        idx = (start_idx + step) % 9
        antar_meta = DASHA_ORDER[idx]
        antar_years = (maha_years * antar_meta["years"]) / TOTAL_DASHA_YEARS
        antar_end = c_dt + timedelta(days=antar_years * days_in_year)

        # Cap at mahadasha end
        if antar_end > maha_end or step == 8:
            antar_end = maha_end

        antardashas.append({
            "level": 2,
            "planet": antar_meta["planet"],
            "mahadasha_planet": maha_planet,
            "duration_years": round(antar_years, 3),
            "start_date": c_dt.isoformat(),
            "end_date": antar_end.isoformat()
        })
        c_dt = antar_end

    return antardashas


def get_active_dasha(mahadashas: list[dict], target_dt: datetime | None = None) -> dict:
    """
    Identifies the active Mahadasha and Antardasha for a given target timestamp (defaults to now).
    """
    if target_dt is None:
        target_dt = datetime.now(birth_tz := pytz.UTC)

    target_iso = target_dt.isoformat()

    active_maha = None
    active_antar = None

    for m in mahadashas:
        if m["start_date"] <= target_iso <= m["end_date"]:
            active_maha = m
            for a in m["antardashas"]:
                if a["start_date"] <= target_iso <= a["end_date"]:
                    active_antar = a
                    break
            break

    return {
        "target_date": target_iso,
        "active_mahadasha": active_maha["planet"] if active_maha else None,
        "active_antardasha": active_antar["planet"] if active_antar else None,
        "mahadasha_period": {"start": active_maha["start_date"], "end": active_maha["end_date"]} if active_maha else None,
        "antardasha_period": {"start": active_antar["start_date"], "end": active_antar["end_date"]} if active_antar else None
    }

