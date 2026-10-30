"""
Prediction Synthesis & Domain Scoring Engine.
Generates quantitative ratings (0-100) and explainable canonical readings 
across 6 primary life domains by evaluating house lords, karakas, yogas, and active dashas.
"""

from app.core.constants import SIGN_LORDS

DIGNITY_WEIGHTS = {
    "Exalted": 25,
    "Moolatrikona": 20,
    "Own Sign": 18,
    "Friendly": 12,
    "Neutral": 8,
    "Enemy": 4,
    "Debilitated": -15
}


def _score_planet(planet_data: dict) -> float:
    """Computes a baseline vitality score for an individual planet."""
    base = 50.0
    dignity_bonus = DIGNITY_WEIGHTS.get(planet_data["dignity"], 8)
    base += dignity_bonus

    if planet_data["is_combust"]:
        base -= 12.0
    if planet_data["is_retrograde"] and planet_data["name"] not in ["Rahu", "Ketu"]:
        # Retrograde natural benefics gain chesta bala (effort power)
        base += 6.0

    return max(10.0, min(100.0, base))


def synthesize_predictions(chart: dict, houses: list[dict], yogas: list[dict], active_dasha: dict) -> dict:
    """
    Computes domain scores (0-100) and structured interpretations for:
    1. Career & Profession (Karma)
    2. Wealth & Finances (Artha)
    3. Health & Vitality (Arogya)
    4. Love & Relationships (Vivaha/Kama)
    5. Intellect & Education (Buddhi)
    6. Spiritual Growth & Mental Peace (Moksha)
    """
    planets = chart["planets"]
    asc = chart["ascendant"]
    h_lords = {h["house_number"]: h["lord"] for h in houses}

    # 1. Career (10th House, 10th Lord, Sun, Saturn)
    lord_10 = h_lords[10]
    p_10_score = _score_planet(planets[lord_10])
    sun_score = _score_planet(planets["Sun"])
    sat_score = _score_planet(planets["Saturn"])
    career_score = round(0.45 * p_10_score + 0.30 * sun_score + 0.25 * sat_score, 1)

    # 2. Wealth (2nd & 11th Houses, Jupiter, Venus)
    lord_2 = h_lords[2]
    lord_11 = h_lords[11]
    p_2_score = _score_planet(planets[lord_2])
    p_11_score = _score_planet(planets[lord_11])
    jup_score = _score_planet(planets["Jupiter"])
    wealth_score = round(0.35 * p_2_score + 0.35 * p_11_score + 0.30 * jup_score, 1)

    # 3. Health & Vitality (1st House / Lagna Lord, 6th House, Mars)
    lord_1 = h_lords[1]
    lord_6 = h_lords[6]
    p_1_score = _score_planet(planets[lord_1])
    mars_score = _score_planet(planets["Mars"])
    health_score = round(0.50 * p_1_score + 0.30 * sun_score + 0.20 * mars_score, 1)

    # 4. Relationships (7th House / 7th Lord, Venus)
    lord_7 = h_lords[7]
    p_7_score = _score_planet(planets[lord_7])
    venus_score = _score_planet(planets["Venus"])
    rel_score = round(0.55 * p_7_score + 0.45 * venus_score, 1)

    # 5. Intellect & Education (5th House / 5th Lord, Mercury)
    lord_5 = h_lords[5]
    p_5_score = _score_planet(planets[lord_5])
    merc_score = _score_planet(planets["Mercury"])
    intellect_score = round(0.50 * p_5_score + 0.50 * merc_score, 1)

    # 6. Spirituality & Inner Peace (9th & 12th Houses, Ketu, Moon)
    lord_9 = h_lords[9]
    lord_12 = h_lords[12]
    p_9_score = _score_planet(planets[lord_9])
    moon_score = _score_planet(planets["Moon"])
    spirituality_score = round(0.40 * p_9_score + 0.35 * moon_score + 0.25 * _score_planet(planets["Ketu"]), 1)

    # Bonus adjustments from Yogas
    for y in yogas:
        if "Raja" in y["name"] or "Mahapurusha" in y["name"]:
            career_score = min(100.0, career_score + 4.0)
        if "Dhana" in y["name"] or "Gajakesari" in y["name"]:
            wealth_score = min(100.0, wealth_score + 5.0)
        if "Budhaditya" in y["name"]:
            intellect_score = min(100.0, intellect_score + 4.0)
        if "Mangal Dosha" in y["name"] and "Cancelled" not in y["description"]:
            rel_score = max(20.0, rel_score - 6.0)

    # Modulate scores with active Dasha lord
    active_maha = active_dasha.get("active_mahadasha")
    dasha_highlight = ""
    if active_maha and active_maha in planets:
        maha_h = planets[active_maha]["house"]
        dasha_highlight = f"Active Mahadasha of {active_maha} (placed in House {maha_h}) strongly activates the life areas governed by House {maha_h}."

    # Synthesize explainable narrative readings
    readings = {
        "career": {
            "score": career_score,
            "status": "Exceptional" if career_score >= 80 else ("Strong" if career_score >= 65 else "Developing"),
            "lord_analysis": f"10th house is governed by {lord_10} (in {planets[lord_10]['sign_name']}, House {planets[lord_10]['house']}, dignity: {planets[lord_10]['dignity']}).",
            "prediction": f"Professional authority and vocational growth are supported by {lord_10}'s position. Natural leadership stems from Sun in {planets['Sun']['sign_name']}.",
            "recommended_focus": "Lead projects with clear autonomy, structure your long-term milestones, and cultivate mentors."
        },
        "wealth": {
            "score": wealth_score,
            "status": "Abundant" if wealth_score >= 80 else ("Prosperous" if wealth_score >= 65 else "Stable"),
            "lord_analysis": f"Assets lord ({lord_2}) in House {planets[lord_2]['house']} with gains lord ({lord_11}) in House {planets[lord_11]['house']}.",
            "prediction": f"Financial accumulation shows strong momentum through {lord_2} and natural significator Jupiter ({planets['Jupiter']['dignity']}).",
            "recommended_focus": "Prioritize high-yield compounding investments and diversify asset holdings."
        },
        "health": {
            "score": health_score,
            "status": "Robust" if health_score >= 80 else ("Balanced" if health_score >= 65 else "Requires Care"),
            "lord_analysis": f"Lagna lord {lord_1} occupies House {planets[lord_1]['house']} ({planets[lord_1]['dignity']}).",
            "prediction": f"Physical constitution and recovery stamina are anchored by your Ascendant in {asc['sign_name']} and {lord_1}'s strength.",
            "recommended_focus": "Maintain circadian consistency, hydration, and rhythmic cardiovascular activity."
        },
        "relationships": {
            "score": rel_score,
            "status": "Harmonious" if rel_score >= 80 else ("Dynamic" if rel_score >= 60 else "Transformational"),
            "lord_analysis": f"7th house of union ruled by {lord_7} in House {planets[lord_7]['house']} with Venus in {planets['Venus']['sign_name']}.",
            "prediction": f"Partnerships are a mirror for personal evolution. Venus in {planets['Venus']['dignity']} guides attraction and mutual harmony.",
            "recommended_focus": "Focus on empathetic listening and transparent expectations with your partner."
        },
        "intellect": {
            "score": intellect_score,
            "status": "Brilliant" if intellect_score >= 80 else ("Sharp" if intellect_score >= 65 else "Practical"),
            "lord_analysis": f"5th house of creativity ruled by {lord_5} with Mercury in {planets['Mercury']['sign_name']}.",
            "prediction": f"Analytical depth and problem-solving abilities are heightened. Excellent capacity for strategic synthesis and retention.",
            "recommended_focus": "Channel mental acuity into mastering high-leverage domains and writing."
        },
        "spirituality": {
            "score": spirituality_score,
            "status": "Profound" if spirituality_score >= 80 else ("Awakening" if spirituality_score >= 65 else "Grounding"),
            "lord_analysis": f"Dharma 9th house ruled by {lord_9} with Moon in Nakshatra {planets['Moon']['nakshatra']['name']}.",
            "prediction": "Inner peace deepens as you align daily actions with personal dharma and philosophical introspection.",
            "recommended_focus": "Daily silent meditation, self-reflection, and nature immersions."
        }
    }

    return {
        "domain_scores": {
            "career": career_score,
            "wealth": wealth_score,
            "health": health_score,
            "relationships": rel_score,
            "intellect": intellect_score,
            "spirituality": spirituality_score
        },
        "dasha_highlight": dasha_highlight,
        "readings": readings
    }

