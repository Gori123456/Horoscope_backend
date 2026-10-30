"""
Transit (Gochar) & Sade Sati Engine.
Calculates real-time planetary transits relative to natal Moon and Ascendant,
evaluating Saturn's Sade Sati phases, Kantaka Shani, and Jupiter Gochar.
"""

from datetime import datetime, timezone
from app.core.astronomy import calculate_julian_day, calculate_lahiri_ayanamsha, calculate_all_planets
from app.core.constants import ZODIAC_SIGNS

def evaluate_transits(natal_moon_sign_id: int, natal_asc_sign_id: int, target_dt: datetime | None = None) -> dict:
    """
    Evaluates real-time transits against the birth chart.
    """
    if target_dt is None:
        target_dt = datetime.now(timezone.utc)

    jd = calculate_julian_day(target_dt)
    ayanamsha = calculate_lahiri_ayanamsha(jd)
    current_planets = calculate_all_planets(jd, ayanamsha)

    # Current signs of key slow-moving transit planets
    sat_deg = current_planets["Saturn"]["sidereal_longitude"]
    sat_sign = int(sat_deg // 30) + 1

    jup_deg = current_planets["Jupiter"]["sidereal_longitude"]
    jup_sign = int(jup_deg // 30) + 1

    rahu_deg = current_planets["Rahu"]["sidereal_longitude"]
    rahu_sign = int(rahu_deg // 30) + 1

    # 1. Saturn Sade Sati Evaluation (relative to Moon)
    sat_from_moon = ((sat_sign - natal_moon_sign_id) % 12) + 1
    sade_sati_status = {
        "is_active": False,
        "phase": "None",
        "house_from_moon": sat_from_moon,
        "description": "No active Sade Sati at this time."
    }

    if sat_from_moon == 12:
        sade_sati_status = {
            "is_active": True,
            "phase": "Phase 1: Rising / Beginning",
            "house_from_moon": 12,
            "description": "Saturn transits the 12th house from natal Moon. Represents mental re-orientation, shedding outlived baggage, and planning long-term foundations."
        }
    elif sat_from_moon == 1:
        sade_sati_status = {
            "is_active": True,
            "phase": "Phase 2: Peak / Core",
            "house_from_moon": 1,
            "description": "Saturn transits natal Moon directly. High focus on self-discipline, inner maturity, character strengthening, and major personal restructuring."
        }
    elif sat_from_moon == 2:
        sade_sati_status = {
            "is_active": True,
            "phase": "Phase 3: Setting / Completion",
            "house_from_moon": 2,
            "description": "Saturn transits 2nd house from natal Moon. Culmination of the cycle; lessons consolidate into financial and domestic stability."
        }
    elif sat_from_moon == 4:
        sade_sati_status = {
            "is_active": False,
            "phase": "Kantaka Shani (4th from Moon)",
            "house_from_moon": 4,
            "description": "Saturn transits 4th from Moon; calls for attention to home environment, emotional center, and sustained patience."
        }
    elif sat_from_moon == 8:
        sade_sati_status = {
            "is_active": False,
            "phase": "Ashtama Shani (8th from Moon)",
            "house_from_moon": 8,
            "description": "Saturn transits 8th from Moon; an inward period demanding prudence, health care, and psychological fortitude."
        }

    # 2. Jupiter Transit (Guru Gochar)
    jup_from_moon = ((jup_sign - natal_moon_sign_id) % 12) + 1
    benefic_houses = [2, 5, 7, 9, 11]
    is_jup_benefic = jup_from_moon in benefic_houses
    jup_status = {
        "transiting_sign": ZODIAC_SIGNS[jup_sign - 1]["name"],
        "house_from_moon": jup_from_moon,
        "is_benefic_transit": is_jup_benefic,
        "description": f"Jupiter transits House {jup_from_moon} from your natal Moon sign. " + (
            "A prime cycle of expansion, social favor, financial growth, and divine timing!" if is_jup_benefic else
            "An inward phase of study, preparation, and spiritual consolidation."
        )
    }

    return {
        "as_of_date": target_dt.isoformat(),
        "transiting_positions": {
            "Saturn": {"sign": ZODIAC_SIGNS[sat_sign - 1]["name"], "degree": sat_deg % 30.0},
            "Jupiter": {"sign": ZODIAC_SIGNS[jup_sign - 1]["name"], "degree": jup_deg % 30.0},
            "Rahu": {"sign": ZODIAC_SIGNS[rahu_sign - 1]["name"], "degree": rahu_deg % 30.0}
        },
        "sade_sati": sade_sati_status,
        "jupiter_gochar": jup_status
    }

