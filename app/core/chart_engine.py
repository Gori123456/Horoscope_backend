"""
Chart Computation Engine (D1 Rashi & D9 Navamsha).
Calculates Signs, Degrees, Nakshatras, Padas, Planetary Dignities, 
Combustion, and Divisional Charts.
"""

from app.core.constants import ZODIAC_SIGNS, NAKSHATRAS, PLANETS, SIGN_LORDS

# Combustion limits from the Sun (in degrees)
COMBUSTION_LIMITS = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,
    "Jupiter": 11.0,
    "Venus": 10.0,
    "Saturn": 15.0
}

def get_nakshatra_info(sidereal_deg: float) -> dict:
    """
    Finds the Nakshatra (0 to 26), Pada (1 to 4), and remaining balance degree.
    """
    norm_deg = sidereal_deg % 360.0
    nak_span = 360.0 / 27.0  # 13° 20' = 13.33333333°
    pada_span = nak_span / 4.0  # 3° 20' = 3.33333333°

    nak_index = int(norm_deg // nak_span)
    nak_meta = NAKSHATRAS[nak_index]

    degree_in_nak = norm_deg - (nak_index * nak_span)
    pada = int(degree_in_nak // pada_span) + 1

    return {
        "nakshatra_id": nak_index,
        "name": nak_meta["name"],
        "lord": nak_meta["lord"],
        "deity": nak_meta["deity"],
        "gana": nak_meta["gana"],
        "pada": pada,
        "degree_in_nakshatra": degree_in_nak,
        "nakshatra_fraction_elapsed": degree_in_nak / nak_span
    }


def calculate_navamsha_sign(sidereal_deg: float) -> int:
    """
    Calculates the D9 (Navamsha) Rashi (1 to 12) for a given sidereal longitude.
    Rules:
    - Fire signs (Aries 1, Leo 5, Sag 9): Navamsha starts from Aries (1).
    - Earth signs (Taurus 2, Virgo 6, Cap 10): Navamsha starts from Capricorn (10).
    - Air signs (Gemini 3, Libra 7, Aqu 11): Navamsha starts from Libra (7).
    - Water signs (Cancer 4, Scorpio 8, Pis 12): Navamsha starts from Cancer (4).
    """
    rashi_index = int(sidereal_deg // 30) + 1  # 1 to 12
    deg_in_sign = sidereal_deg % 30.0
    navamsha_part = int(deg_in_sign // (30.0 / 9.0))  # 0 to 8

    # Base starting sign based on element
    if rashi_index in [1, 5, 9]:
        base_sign = 1  # Aries
    elif rashi_index in [2, 6, 10]:
        base_sign = 10  # Capricorn
    elif rashi_index in [3, 7, 11]:
        base_sign = 7  # Libra
    else:
        base_sign = 4  # Cancer

    navamsha_sign = ((base_sign - 1 + navamsha_part) % 12) + 1
    return navamsha_sign


def evaluate_dignity(planet_name: str, sign_id: int, deg_in_sign: float) -> str:
    """
    Evaluates the classical dignity of a planet:
    - Exalted (Uchcha)
    - Moolatrikona
    - Own Sign (Swakshetra)
    - Great Friend / Friend
    - Neutral
    - Enemy / Great Enemy
    - Debilitated (Neecha)
    """
    if planet_name not in PLANETS:
        return "Neutral"

    p_meta = PLANETS[planet_name]

    # Exalted
    if sign_id == p_meta.get("exalted_sign"):
        return "Exalted"

    # Debilitated
    if sign_id == p_meta.get("debilitated_sign"):
        return "Debilitated"

    # Moolatrikona
    m_sign = p_meta.get("moolatrikona_sign")
    m_range = p_meta.get("moolatrikona_range")
    if m_sign == sign_id and m_range and m_range[0] <= deg_in_sign <= m_range[1]:
        return "Moolatrikona"

    # Own Sign
    if sign_id in p_meta.get("own_signs", []):
        return "Own Sign"

    # Relationship with sign lord
    sign_lord = SIGN_LORDS[sign_id]
    if sign_lord == planet_name:
        return "Own Sign"

    if sign_lord in p_meta.get("friends", []):
        return "Friendly"
    elif sign_lord in p_meta.get("enemies", []):
        return "Enemy"
    else:
        return "Neutral"


def check_combustion(planet_name: str, planet_deg: float, sun_deg: float) -> bool:
    """Checks whether an inner or outer planet is combust by proximity to the Sun."""
    if planet_name not in COMBUSTION_LIMITS:
        return False

    limit = COMBUSTION_LIMITS[planet_name]
    diff = abs(planet_deg - sun_deg) % 360.0
    if diff > 180.0:
        diff = 360.0 - diff

    return diff <= limit


def build_full_chart(raw_planets: dict[str, dict], ascendant_meta: dict) -> dict:
    """
    Constructs the complete D1 (Rashi) and D9 (Navamsha) charts with 
    house positions, nakshatras, dignities, and combustion flags.
    """
    asc_deg = ascendant_meta["sidereal_ascendant"]
    asc_sign_id = int(asc_deg // 30) + 1
    asc_sign_meta = ZODIAC_SIGNS[asc_sign_id - 1]
    asc_nak = get_nakshatra_info(asc_deg)
    asc_d9_sign_id = calculate_navamsha_sign(asc_deg)

    chart = {
        "ascendant": {
            "longitude": asc_deg,
            "sign_id": asc_sign_id,
            "sign_name": asc_sign_meta["name"],
            "sign_sanskrit": asc_sign_meta["sanskrit"],
            "degree_in_sign": asc_deg % 30.0,
            "nakshatra": asc_nak,
            "navamsha_sign_id": asc_d9_sign_id,
            "navamsha_sign_name": ZODIAC_SIGNS[asc_d9_sign_id - 1]["name"]
        },
        "planets": {}
    }

    sun_deg = raw_planets["Sun"]["sidereal_longitude"]

    for p_name, p_data in raw_planets.items():
        sid_deg = p_data["sidereal_longitude"]
        sign_id = int(sid_deg // 30) + 1
        sign_meta = ZODIAC_SIGNS[sign_id - 1]
        deg_in_sign = sid_deg % 30.0
        nak_info = get_nakshatra_info(sid_deg)
        d9_sign_id = calculate_navamsha_sign(sid_deg)
        house_num = ((sign_id - asc_sign_id) % 12) + 1
        dignity = evaluate_dignity(p_name, sign_id, deg_in_sign)
        is_combust = check_combustion(p_name, sid_deg, sun_deg)

        chart["planets"][p_name] = {
            "name": p_name,
            "sanskrit": PLANETS[p_name]["sanskrit"],
            "sidereal_longitude": sid_deg,
            "sign_id": sign_id,
            "sign_name": sign_meta["name"],
            "sign_sanskrit": sign_meta["sanskrit"],
            "degree_in_sign": deg_in_sign,
            "house": house_num,
            "nakshatra": nak_info,
            "dignity": dignity,
            "is_retrograde": p_data["is_retrograde"],
            "is_combust": is_combust,
            "navamsha_sign_id": d9_sign_id,
            "navamsha_sign_name": ZODIAC_SIGNS[d9_sign_id - 1]["name"]
        }

    return chart

