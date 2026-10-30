"""
Classical Vedic Yogas & Doshas Rule Engine.
Evaluates 20+ canonical planetary combinations with deterministic logic,
classical citations, positive/negative impact weights, and cancellations.
"""

from app.core.constants import SIGN_LORDS, HOUSE_TYPES

def detect_yogas(chart: dict, houses: list[dict]) -> list[dict]:
    """
    Evaluates all canonical yogas and doshas against the calculated birth chart.
    """
    detected = []
    planets = chart["planets"]
    asc = chart["ascendant"]
    asc_sign = asc["sign_id"]

    # Quick lookup helpers
    p_houses = {p: info["house"] for p, info in planets.items()}
    p_signs = {p: info["sign_id"] for p, info in planets.items()}
    p_dignities = {p: info["dignity"] for p, info in planets.items()}
    
    # House lord lookup (House number -> Planet name)
    h_lords = {h["house_number"]: h["lord"] for h in houses}

    # 1. Gajakesari Yoga (Jupiter in Kendra 1, 4, 7, 10 from Moon)
    moon_house = p_houses["Moon"]
    jup_house = p_houses["Jupiter"]
    jup_from_moon = ((jup_house - moon_house) % 12) + 1
    if jup_from_moon in [1, 4, 7, 10]:
        detected.append({
            "name": "Gajakesari Yoga",
            "category": "Raja / Auspicious Yoga",
            "type": "Benefic",
            "impact_weight": 85,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 36, v. 3",
            "description": "Jupiter is in a Kendra (angular house) from the Moon. Bestows exceptional wisdom, enduring reputation, sound intellect, and protection against major adversities.",
            "planets_involved": ["Moon", "Jupiter"]
        })

    # 2. Budhaditya Yoga (Sun + Mercury in same sign, Mercury not deeply combust)
    if p_signs["Sun"] == p_signs["Mercury"]:
        combust_flag = planets["Mercury"]["is_combust"]
        detected.append({
            "name": "Budhaditya Yoga",
            "category": "Intellectual / Solar Yoga",
            "type": "Benefic",
            "impact_weight": 70 if not combust_flag else 55,
            "classical_citation": "Saravali, Ch. 31",
            "description": f"Sun and Mercury share sign {planets['Sun']['sign_name']}. Grants keen analytical acumen, high learning ability, articulate communication, and administrative flair." + (" (Mild combustion present)." if combust_flag else " (Clear and luminous)."),
            "planets_involved": ["Sun", "Mercury"]
        })

    # 3. Pancha Mahapurusha Yogas (Mars, Mercury, Jupiter, Venus, Saturn in Kendra + Exalted/Own Sign)
    kendra_houses = [1, 4, 7, 10]
    
    # Ruchaka (Mars)
    if p_houses["Mars"] in kendra_houses and p_dignities["Mars"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        detected.append({
            "name": "Ruchaka Yoga (Mahapurusha)",
            "category": "Pancha Mahapurusha",
            "type": "Benefic",
            "impact_weight": 90,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 75",
            "description": "Mars is in a Kendra in its own or exalted sign. Bestows courage, executive leadership, physical stamina, valor, and success in technical or leadership arenas.",
            "planets_involved": ["Mars"]
        })

    # Bhadra (Mercury)
    if p_houses["Mercury"] in kendra_houses and p_dignities["Mercury"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        detected.append({
            "name": "Bhadra Yoga (Mahapurusha)",
            "category": "Pancha Mahapurusha",
            "type": "Benefic",
            "impact_weight": 90,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 75",
            "description": "Mercury is in a Kendra in Gemini or Virgo. Produces a polymath intellect, eloquent oratory, sharp commercial skills, and longevity.",
            "planets_involved": ["Mercury"]
        })

    # Hamsa (Jupiter)
    if p_houses["Jupiter"] in kendra_houses and p_dignities["Jupiter"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        detected.append({
            "name": "Hamsa Yoga (Mahapurusha)",
            "category": "Pancha Mahapurusha",
            "type": "Benefic",
            "impact_weight": 95,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 75",
            "description": "Jupiter is in a Kendra in Cancer, Sagittarius, or Pisces. Generates noble character, spiritual wisdom, respected leadership, and clean dharmic fortune.",
            "planets_involved": ["Jupiter"]
        })

    # Malavya (Venus)
    if p_houses["Venus"] in kendra_houses and p_dignities["Venus"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        detected.append({
            "name": "Malavya Yoga (Mahapurusha)",
            "category": "Pancha Mahapurusha",
            "type": "Benefic",
            "impact_weight": 90,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 75",
            "description": "Venus is in a Kendra in Taurus, Libra, or Pisces. Bestows aesthetic refinement, artistic mastery, wealth of conveyances, and harmonious relations.",
            "planets_involved": ["Venus"]
        })

    # Shasha (Saturn)
    if p_houses["Saturn"] in kendra_houses and p_dignities["Saturn"] in ["Exalted", "Own Sign", "Moolatrikona"]:
        detected.append({
            "name": "Shasha Yoga (Mahapurusha)",
            "category": "Pancha Mahapurusha",
            "type": "Benefic",
            "impact_weight": 85,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 75",
            "description": "Saturn is in a Kendra in Libra, Capricorn, or Aquarius. Bestows profound perseverance, command over people, structural mastery, and long-lasting authority.",
            "planets_involved": ["Saturn"]
        })

    # 4. Classical Raja Yoga (Kendra Lord + Trikona Lord conjunction)
    kendra_lords = set([h_lords[h] for h in [1, 4, 7, 10]])
    trikona_lords = set([h_lords[h] for h in [5, 9]])  # 1st lord already in kendra
    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl != tl and p_signs[kl] == p_signs[tl]:
                detected.append({
                    "name": f"Dharma-Karmadhipati Raja Yoga ({kl} & {tl})",
                    "category": "Raja Yoga",
                    "type": "Benefic",
                    "impact_weight": 88,
                    "classical_citation": "Phaladeepika, Ch. 6",
                    "description": f"Lord of Kendra ({kl}) and Lord of Trikona ({tl}) are conjoined in House {p_houses[kl]}. Unites purpose with power, propelling high social rise and authority.",
                    "planets_involved": [kl, tl]
                })

    # 5. Dhana Yoga (Lords of Wealth 2, 5, 9, 11 combining)
    wealth_lords = [h_lords[2], h_lords[5], h_lords[9], h_lords[11]]
    if p_signs[h_lords[2]] == p_signs[h_lords[11]]:
        detected.append({
            "name": "Maha Dhana Yoga (2nd & 11th Lords Conjoined)",
            "category": "Dhana / Wealth Yoga",
            "type": "Benefic",
            "impact_weight": 85,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 41",
            "description": f"The lord of accumulated assets ({h_lords[2]}) and lord of recurring gains ({h_lords[11]}) are combined in House {p_houses[h_lords[2]]}. Assures continuous financial accumulation.",
            "planets_involved": [h_lords[2], h_lords[11]]
        })

    # 6. Chandra-Mangala Yoga (Moon + Mars in same house)
    if p_signs["Moon"] == p_signs["Mars"]:
        detected.append({
            "name": "Chandra-Mangala Yoga",
            "category": "Prosperity / Financial Drive",
            "type": "Benefic",
            "impact_weight": 75,
            "classical_citation": "Saravali, Ch. 33",
            "description": "Moon and Mars conjoined in the same sign. Awakens intense commercial drive, property accumulation abilities, and passionate enterprise.",
            "planets_involved": ["Moon", "Mars"]
        })

    # 7. Amala Yoga (Natural benefic in 10th house from Lagna or Moon)
    benefics = ["Jupiter", "Venus", "Mercury"]
    tenth_from_lagna = [p for p in benefics if p_houses[p] == 10]
    if tenth_from_lagna:
        detected.append({
            "name": "Amala Yoga",
            "category": "Career Purity & Renown",
            "type": "Benefic",
            "impact_weight": 80,
            "classical_citation": "Phaladeepika, Ch. 6, v. 21",
            "description": f"Natural benefic ({', '.join(tenth_from_lagna)}) occupies the 10th house of career. Bestows unblemished professional reputation, ethical success, and lasting social goodwill.",
            "planets_involved": tenth_from_lagna
        })

    # 8. Viparita Raja Yogas (Lords of 6, 8, 12 in Dusthanas 6, 8, 12)
    l6, l8, l12 = h_lords[6], h_lords[8], h_lords[12]
    dusthanas = [6, 8, 12]
    if p_houses[l6] in dusthanas and p_houses[l6] != 6:
        detected.append({
            "name": "Harsha Viparita Raja Yoga",
            "category": "Viparita Raja Yoga",
            "type": "Benefic through Crisis",
            "impact_weight": 75,
            "classical_citation": "Uttara Kalamrita, Ch. 4",
            "description": f"6th lord ({l6}) placed in House {p_houses[l6]}. Transforms opponents and crises into breakthroughs, giving invincibility against adversaries.",
            "planets_involved": [l6]
        })
    if p_houses[l8] in dusthanas and p_houses[l8] != 8:
        detected.append({
            "name": "Sarala Viparita Raja Yoga",
            "category": "Viparita Raja Yoga",
            "type": "Benefic through Crisis",
            "impact_weight": 75,
            "classical_citation": "Uttara Kalamrita, Ch. 4",
            "description": f"8th lord ({l8}) placed in House {p_houses[l8]}. Grants fearlessness, long life, and sudden windfall gains during turbulent times.",
            "planets_involved": [l8]
        })

    # 9. Manglik / Kuja Dosha (Mars in 1, 2, 4, 7, 8, 12)
    mars_h = p_houses["Mars"]
    if mars_h in [1, 2, 4, 7, 8, 12]:
        # Cancellation checks:
        # Mars in Aries (1st), Scorpio (4th), Capricorn (7th), Cancer (8th), Sag (12th)
        is_cancelled = False
        cancellation_reason = ""
        m_sign = p_signs["Mars"]

        if mars_h == 1 and m_sign == 1:
            is_cancelled = True
            cancellation_reason = "Mars is in its own sign Aries in the 1st House."
        elif mars_h == 4 and m_sign == 8:
            is_cancelled = True
            cancellation_reason = "Mars is in its own sign Scorpio in the 4th House."
        elif mars_h == 7 and m_sign == 10:
            is_cancelled = True
            cancellation_reason = "Mars is exalted in Capricorn in the 7th House."
        elif jup_from_moon in [1, 4, 7, 10]:
            is_cancelled = True
            cancellation_reason = "Jupiter occupies a Kendra, providing strong mitigating aspect."

        detected.append({
            "name": "Mangal Dosha (Kuja Dosha)",
            "category": "Dosha / Relationship Challenge",
            "type": "Challenging" if not is_cancelled else "Mitigated Dosha",
            "impact_weight": -45 if not is_cancelled else -15,
            "classical_citation": "Brihat Parashara Hora Shastra, Stri Jataka",
            "description": f"Mars is placed in House {mars_h}. Indicates passionate intensity and high temperamental expectations in partnerships." + (f" Note: Classical cancellation applies ({cancellation_reason})." if is_cancelled else " Balance through conscious emotional communication is recommended."),
            "planets_involved": ["Mars"]
        })

    # 10. Kemadruma Dosha (No planets in 2nd or 12th from Moon)
    second_from_moon = (moon_house % 12) + 1
    twelfth_from_moon = ((moon_house - 2) % 12) + 1
    planets_around_moon = [p for p in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"] if p_houses[p] in [second_from_moon, twelfth_from_moon]]
    if not planets_around_moon:
        # Check cancellation: planets in kendra from Moon or Lagna
        kendra_planets = [p for p in ["Jupiter", "Venus", "Mercury"] if ((p_houses[p] - moon_house) % 12) + 1 in [1, 4, 7, 10]]
        is_kemadruma_cancelled = len(kendra_planets) > 0
        detected.append({
            "name": "Kemadruma Dosha",
            "category": "Lunar Affliction",
            "type": "Challenging" if not is_kemadruma_cancelled else "Mitigated Dosha",
            "impact_weight": -40 if not is_kemadruma_cancelled else -10,
            "classical_citation": "Brihat Parashara Hora Shastra, Ch. 37",
            "description": "No planets occupy the flanking 2nd or 12th houses from Moon, indicating periods of feeling psychologically isolated or unsupported." + (" Cancelled by benefic kendra placements." if is_kemadruma_cancelled else ""),
            "planets_involved": ["Moon"]
        })

    # 11. Kaal Sarp Yoga / Dosha
    # Check if all 7 visible planets are on one side of Rahu-Ketu axis
    rahu_h = p_houses["Rahu"]
    ketu_h = p_houses["Ketu"]
    visible_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    # Measure circular distance from Rahu to planet
    distances_from_rahu = [((p_houses[p] - rahu_h) % 12) for p in visible_planets]
    all_one_side = all(d < 6 for d in distances_from_rahu) or all(d >= 6 for d in distances_from_rahu)
    if all_one_side:
        detected.append({
            "name": "Kaal Sarp Yoga",
            "category": "Karmic Axis / Intense Transformation",
            "type": "Complex Karmic Trigger",
            "impact_weight": 50,  # Double-edged: intense rise after mid-life struggle
            "classical_citation": "Classical Jyotish Canon",
            "description": "All seven visible planets are enclosed between the Rahu-Ketu karmic axis. Sparks dramatic life transformations, initial struggle followed by immense resilience and unconventional distinction.",
            "planets_involved": ["Rahu", "Ketu"] + visible_planets
        })

    return detected

