"""
Houses (Bhavas) Computation Module.
Computes 12 Bhava cusps, assigns signs and house lords, 
and maps planetary placements relative to the Ascendant (Lagna) and Moon (Chandra Lagna).
"""

from app.core.constants import ZODIAC_SIGNS, SIGN_LORDS, HOUSE_TYPES

def calculate_whole_sign_houses(ascendant_sidereal_deg: float) -> list[dict]:
    """
    Computes 12 Bhavas using the Vedic Whole Sign House system.
    House 1 is the entire Rashi (Sign) where the Ascendant falls.
    House 2 is the next Rashi, up to House 12.
    """
    asc_sign_index = int(ascendant_sidereal_deg // 30) + 1  # 1 to 12
    houses = []

    for h_num in range(1, 13):
        sign_id = ((asc_sign_index - 1 + (h_num - 1)) % 12) + 1
        sign_meta = ZODIAC_SIGNS[sign_id - 1]
        lord = SIGN_LORDS[sign_id]
        
        # House classification
        classifications = []
        for c_type, h_list in HOUSE_TYPES.items():
            if h_num in h_list:
                classifications.append(c_type)

        houses.append({
            "house_number": h_num,
            "sign_id": sign_id,
            "sign_name": sign_meta["name"],
            "sign_sanskrit": sign_meta["sanskrit"],
            "lord": lord,
            "start_degree": (sign_id - 1) * 30.0,
            "end_degree": sign_id * 30.0,
            "classifications": classifications
        })

    return houses


def assign_planets_to_houses(planets_data: dict[str, dict], ascendant_sidereal_deg: float) -> dict[str, int]:
    """
    Assigns each planet to its corresponding Bhava (1 to 12) relative to the Ascendant sign.
    """
    asc_sign_index = int(ascendant_sidereal_deg // 30) + 1  # 1 to 12
    placements = {}

    for planet_name, p_info in planets_data.items():
        p_deg = p_info["sidereal_longitude"]
        p_sign_index = int(p_deg // 30) + 1  # 1 to 12
        house_num = ((p_sign_index - asc_sign_index) % 12) + 1
        placements[planet_name] = house_num

    return placements

