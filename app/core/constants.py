"""
Astrological Constants & Canon for Deterministic Vedic (Jyotish) Computation.
All definitions are codified strictly from foundational classical texts:
Brihat Parashara Hora Shastra, Phaladeepika, and Saravali.
"""

# 12 Zodiac Signs (Rashis)
ZODIAC_SIGNS = [
    {"id": 1, "name": "Aries", "sanskrit": "Mesha", "lord": "Mars", "element": "Fire", "modality": "Movable", "symbol": "Ram"},
    {"id": 2, "name": "Taurus", "sanskrit": "Vrishabha", "lord": "Venus", "element": "Earth", "modality": "Fixed", "symbol": "Bull"},
    {"id": 3, "name": "Gemini", "sanskrit": "Mithuna", "lord": "Mercury", "element": "Air", "modality": "Dual", "symbol": "Twins"},
    {"id": 4, "name": "Cancer", "sanskrit": "Karka", "lord": "Moon", "element": "Water", "modality": "Movable", "symbol": "Crab"},
    {"id": 5, "name": "Leo", "sanskrit": "Simha", "lord": "Sun", "element": "Fire", "modality": "Fixed", "symbol": "Lion"},
    {"id": 6, "name": "Virgo", "sanskrit": "Kanya", "lord": "Mercury", "element": "Earth", "modality": "Dual", "symbol": "Maiden"},
    {"id": 7, "name": "Libra", "sanskrit": "Tula", "lord": "Venus", "element": "Air", "modality": "Movable", "symbol": "Scales"},
    {"id": 8, "name": "Scorpio", "sanskrit": "Vrischika", "lord": "Mars", "element": "Water", "modality": "Fixed", "symbol": "Scorpion"},
    {"id": 9, "name": "Sagittarius", "sanskrit": "Dhanu", "lord": "Jupiter", "element": "Fire", "modality": "Dual", "symbol": "Archer / Centaur"},
    {"id": 10, "name": "Capricorn", "sanskrit": "Makara", "lord": "Saturn", "element": "Earth", "modality": "Movable", "symbol": "Sea-Goat"},
    {"id": 11, "name": "Aquarius", "sanskrit": "Kumbha", "lord": "Saturn", "element": "Air", "modality": "Fixed", "symbol": "Water-Bearer"},
    {"id": 12, "name": "Pisces", "sanskrit": "Meena", "lord": "Jupiter", "element": "Water", "modality": "Dual", "symbol": "Fishes"}
]

# 27 Nakshatras (Lunar Mansions)
NAKSHATRAS = [
    {"id": 0, "name": "Ashwini", "lord": "Ketu", "start_deg": 0.0, "end_deg": 13.333333, "deity": "Ashwini Kumaras", "gana": "Deva"},
    {"id": 1, "name": "Bharani", "lord": "Venus", "start_deg": 13.333333, "end_deg": 26.666667, "deity": "Yama", "gana": "Manushya"},
    {"id": 2, "name": "Krittika", "lord": "Sun", "start_deg": 26.666667, "end_deg": 40.0, "deity": "Agni", "gana": "Rakshasa"},
    {"id": 3, "name": "Rohini", "lord": "Moon", "start_deg": 40.0, "end_deg": 53.333333, "deity": "Brahma", "gana": "Manushya"},
    {"id": 4, "name": "Mrigashira", "lord": "Mars", "start_deg": 53.333333, "end_deg": 66.666667, "deity": "Soma", "gana": "Deva"},
    {"id": 5, "name": "Ardra", "lord": "Rahu", "start_deg": 66.666667, "end_deg": 80.0, "deity": "Rudra", "gana": "Manushya"},
    {"id": 6, "name": "Punarvasu", "lord": "Jupiter", "start_deg": 80.0, "end_deg": 93.333333, "deity": "Aditi", "gana": "Deva"},
    {"id": 7, "name": "Pushya", "lord": "Saturn", "start_deg": 93.333333, "end_deg": 106.666667, "deity": "Brihaspati", "gana": "Deva"},
    {"id": 8, "name": "Ashlesha", "lord": "Mercury", "start_deg": 106.666667, "end_deg": 120.0, "deity": "Nagas", "gana": "Rakshasa"},
    {"id": 9, "name": "Magha", "lord": "Ketu", "start_deg": 120.0, "end_deg": 133.333333, "deity": "Pitris", "gana": "Rakshasa"},
    {"id": 10, "name": "Purva Phalguni", "lord": "Venus", "start_deg": 133.333333, "end_deg": 146.666667, "deity": "Bhaga", "gana": "Manushya"},
    {"id": 11, "name": "Uttara Phalguni", "lord": "Sun", "start_deg": 146.666667, "end_deg": 160.0, "deity": "Aryaman", "gana": "Manushya"},
    {"id": 12, "name": "Hasta", "lord": "Moon", "start_deg": 160.0, "end_deg": 173.333333, "deity": "Savitr", "gana": "Deva"},
    {"id": 13, "name": "Chitra", "lord": "Mars", "start_deg": 173.333333, "end_deg": 186.666667, "deity": "Tvashtar", "gana": "Rakshasa"},
    {"id": 14, "name": "Swati", "lord": "Rahu", "start_deg": 186.666667, "end_deg": 200.0, "deity": "Vayu", "gana": "Deva"},
    {"id": 15, "name": "Vishakha", "lord": "Jupiter", "start_deg": 200.0, "end_deg": 213.333333, "deity": "Indra-Agni", "gana": "Rakshasa"},
    {"id": 16, "name": "Anuradha", "lord": "Saturn", "start_deg": 213.333333, "end_deg": 226.666667, "deity": "Mitra", "gana": "Deva"},
    {"id": 17, "name": "Jyeshtha", "lord": "Mercury", "start_deg": 226.666667, "end_deg": 240.0, "deity": "Indra", "gana": "Rakshasa"},
    {"id": 18, "name": "Mula", "lord": "Ketu", "start_deg": 240.0, "end_deg": 253.333333, "deity": "Nirriti", "gana": "Rakshasa"},
    {"id": 19, "name": "Purva Ashadha", "lord": "Venus", "start_deg": 253.333333, "end_deg": 266.666667, "deity": "Apas", "gana": "Manushya"},
    {"id": 20, "name": "Uttara Ashadha", "lord": "Sun", "start_deg": 266.666667, "end_deg": 280.0, "deity": "Vishwadevas", "gana": "Manushya"},
    {"id": 21, "name": "Shravana", "lord": "Moon", "start_deg": 280.0, "end_deg": 293.333333, "deity": "Vishnu", "gana": "Deva"},
    {"id": 22, "name": "Dhanishta", "lord": "Mars", "start_deg": 293.333333, "end_deg": 306.666667, "deity": "Ashta Vasus", "gana": "Rakshasa"},
    {"id": 23, "name": "Shatabhisha", "lord": "Rahu", "start_deg": 306.666667, "end_deg": 320.0, "deity": "Varuna", "gana": "Rakshasa"},
    {"id": 24, "name": "Purva Bhadrapada", "lord": "Jupiter", "start_deg": 320.0, "end_deg": 333.333333, "deity": "Aja Ekapada", "gana": "Manushya"},
    {"id": 25, "name": "Uttara Bhadrapada", "lord": "Saturn", "start_deg": 333.333333, "end_deg": 346.666667, "deity": "Ahirbudhnya", "gana": "Manushya"},
    {"id": 26, "name": "Revati", "lord": "Mercury", "start_deg": 346.666667, "end_deg": 360.0, "deity": "Pushan", "gana": "Deva"}
]

# 9 Celestial Bodies (Navagraha) & Dignity Rules
PLANETS = {
    "Sun": {
        "sanskrit": "Surya",
        "nature": "Natural Malefic / Krura",
        "own_signs": [5],            # Leo
        "moolatrikona_sign": 5,
        "moolatrikona_range": (0.0, 20.0),
        "exalted_sign": 1,           # Aries
        "exalted_deep_deg": 10.0,
        "debilitated_sign": 7,       # Libra
        "debilitated_deep_deg": 10.0,
        "friends": ["Moon", "Mars", "Jupiter"],
        "neutral": ["Mercury"],
        "enemies": ["Venus", "Saturn", "Rahu", "Ketu"]
    },
    "Moon": {
        "sanskrit": "Chandra",
        "nature": "Benefic when Waxing / Malefic when Waning",
        "own_signs": [4],            # Cancer
        "moolatrikona_sign": 2,      # Taurus 3° to 30°
        "moolatrikona_range": (3.0, 30.0),
        "exalted_sign": 2,           # Taurus
        "exalted_deep_deg": 3.0,
        "debilitated_sign": 8,       # Scorpio
        "debilitated_deep_deg": 3.0,
        "friends": ["Sun", "Mercury"],
        "neutral": ["Mars", "Jupiter", "Venus", "Saturn"],
        "enemies": ["Rahu", "Ketu"]
    },
    "Mars": {
        "sanskrit": "Mangala",
        "nature": "Natural Malefic",
        "own_signs": [1, 8],         # Aries, Scorpio
        "moolatrikona_sign": 1,      # Aries 0° to 12°
        "moolatrikona_range": (0.0, 12.0),
        "exalted_sign": 10,          # Capricorn
        "exalted_deep_deg": 28.0,
        "debilitated_sign": 4,       # Cancer
        "debilitated_deep_deg": 28.0,
        "friends": ["Sun", "Moon", "Jupiter"],
        "neutral": ["Venus", "Saturn"],
        "enemies": ["Mercury", "Rahu"]
    },
    "Mercury": {
        "sanskrit": "Budha",
        "nature": "Natural Benefic / Adaptable",
        "own_signs": [3, 6],         # Gemini, Virgo
        "moolatrikona_sign": 6,      # Virgo 15° to 20°
        "moolatrikona_range": (15.0, 20.0),
        "exalted_sign": 6,           # Virgo
        "exalted_deep_deg": 15.0,
        "debilitated_sign": 12,      # Pisces
        "debilitated_deep_deg": 15.0,
        "friends": ["Sun", "Venus"],
        "neutral": ["Mars", "Jupiter", "Saturn"],
        "enemies": ["Moon"]
    },
    "Jupiter": {
        "sanskrit": "Guru / Brihaspati",
        "nature": "Great Natural Benefic",
        "own_signs": [9, 12],        # Sagittarius, Pisces
        "moolatrikona_sign": 9,      # Sagittarius 0° to 10°
        "moolatrikona_range": (0.0, 10.0),
        "exalted_sign": 4,           # Cancer
        "exalted_deep_deg": 5.0,
        "debilitated_sign": 10,      # Capricorn
        "debilitated_deep_deg": 5.0,
        "friends": ["Sun", "Moon", "Mars"],
        "neutral": ["Saturn"],
        "enemies": ["Mercury", "Venus"]
    },
    "Venus": {
        "sanskrit": "Shukra",
        "nature": "Natural Benefic",
        "own_signs": [2, 7],         # Taurus, Libra
        "moolatrikona_sign": 7,      # Libra 0° to 15°
        "moolatrikona_range": (0.0, 15.0),
        "exalted_sign": 12,          # Pisces
        "exalted_deep_deg": 27.0,
        "debilitated_sign": 6,       # Virgo
        "debilitated_deep_deg": 27.0,
        "friends": ["Mercury", "Saturn", "Rahu"],
        "neutral": ["Mars", "Jupiter"],
        "enemies": ["Sun", "Moon"]
    },
    "Saturn": {
        "sanskrit": "Shani",
        "nature": "Natural Malefic / Great Taskmaster",
        "own_signs": [10, 11],       # Capricorn, Aquarius
        "moolatrikona_sign": 11,     # Aquarius 0° to 20°
        "moolatrikona_range": (0.0, 20.0),
        "exalted_sign": 7,           # Libra
        "exalted_deep_deg": 20.0,
        "debilitated_sign": 1,       # Aries
        "debilitated_deep_deg": 20.0,
        "friends": ["Mercury", "Venus", "Rahu"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"]
    },
    "Rahu": {
        "sanskrit": "Rahu (North Lunar Node)",
        "nature": "Shadow Planet / Chhaya Graha / Material Illusion",
        "own_signs": [11],           # Aquarius (traditional assignment)
        "moolatrikona_sign": 3,      # Gemini
        "moolatrikona_range": (0.0, 30.0),
        "exalted_sign": 2,           # Taurus
        "exalted_deep_deg": 20.0,
        "debilitated_sign": 8,       # Scorpio
        "debilitated_deep_deg": 20.0,
        "friends": ["Venus", "Saturn", "Mercury"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"]
    },
    "Ketu": {
        "sanskrit": "Ketu (South Lunar Node)",
        "nature": "Shadow Planet / Chhaya Graha / Spiritual Liberation (Moksha)",
        "own_signs": [8],            # Scorpio (traditional assignment)
        "moolatrikona_sign": 9,      # Sagittarius
        "moolatrikona_range": (0.0, 30.0),
        "exalted_sign": 8,           # Scorpio
        "exalted_deep_deg": 20.0,
        "debilitated_sign": 2,       # Taurus
        "debilitated_deep_deg": 20.0,
        "friends": ["Mars", "Venus", "Saturn"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon"]
    }
}

# Vimshottari Dasha 120-Year Planetary Cycles (in order)
DASHA_ORDER = [
    {"planet": "Ketu", "years": 7},
    {"planet": "Venus", "years": 20},
    {"planet": "Sun", "years": 6},
    {"planet": "Moon", "years": 10},
    {"planet": "Mars", "years": 7},
    {"planet": "Rahu", "years": 18},
    {"planet": "Jupiter", "years": 16},
    {"planet": "Saturn", "years": 19},
    {"planet": "Mercury", "years": 17}
]
TOTAL_DASHA_YEARS = 120.0

# 12 Bhavas (Houses) Classifications
HOUSE_TYPES = {
    "Kendra": [1, 4, 7, 10],       # Angular / Pillars of Life
    "Trikona": [1, 5, 9],          # Trinal / Houses of Fortune & Dharma
    "Upachaya": [3, 6, 10, 11],    # Houses of Growth through Effort
    "Dusthana": [6, 8, 12],        # Houses of Challenges, Disease, Transformation, Expense
    "Maraka": [2, 7]               # Killer / Transition Houses
}

# Sign to House Lord mapping helper
SIGN_LORDS = {
    1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
    5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
    9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
}

