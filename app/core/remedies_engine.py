"""
Remedial Measures & Problem-Solving Engine (Upayas).
Analyzes each life stream (Career, Wealth, Relationships, Health, Intellect, and Active Dasha),
detects root astrological afflictions, and prescribes concrete, actionable, step-by-step solutions:
1. Root Astrological Cause (Plain English)
2. Practical Psychological / Daily Habit Correction
3. Classical Vedic Karmic Remedy (Charity, Danam, Energy Rebalancing)
4. Sound Vibration (Mantra / Chanting)
5. Optimal Day, Color & Timing
"""

def generate_stream_remedies(chart: dict, houses: list[dict], yogas: list[dict], active_dasha: dict) -> dict:
    """
    Evaluates every life stream for planetary afflictions and provides
    comprehensive, step-by-step remedial plans to alleviate obstacles.
    """
    planets = chart["planets"]
    asc = chart["ascendant"]
    h_lords = {h["house_number"]: h["lord"] for h in houses}

    remedies_by_stream = {}

    # =========================================================================
    # 1. CAREER & VOCATION STREAM (Karma)
    # =========================================================================
    lord_10 = h_lords[10]
    p_10 = planets[lord_10]
    sun_p = planets["Sun"]
    sat_p = planets["Saturn"]

    career_issues = []
    career_remedies = []

    if p_10["dignity"] in ["Debilitated", "Enemy"] or p_10["is_combust"]:
        career_issues.append(f"10th house lord ({lord_10}) is in {p_10['dignity']} dignity in {p_10['sign_name']}, causing recognition delays and feeling undervalued.")
    if sat_p["house"] in [1, 10] or sat_p["dignity"] == "Debilitated":
        career_issues.append("Saturn's heavy influence indicates heavy workload with delayed rewards; demands systematic discipline.")
    if sun_p["is_combust"] or sun_p["dignity"] == "Debilitated":
        career_issues.append("Sun's position indicates occasional friction with superiors, bureaucratic delays, or imposter syndrome.")

    if not career_issues:
        career_status = "Smooth & Favorable"
        career_core_problem = "Minor day-to-day work stress; career foundation is inherently supportive."
        action_step = "Take executive initiative. Document project milestones and present your impact transparently to leadership."
        vedic_remedy = "Offer water (Arghya) to the rising morning Sun from a copper vessel at sunrise to amplify executive aura."
        mantra = "Om Hram Hreem Hroum Sah Suryaya Namaha (11 times at sunrise)."
        charity = "Donate whole wheat grain or jaggery (gur) on Sundays."
        lucky_timing = "Sunday mornings, wear warm tones (Copper, Crimson, Gold)."
    else:
        career_status = "Challenging / Needs Action"
        career_core_problem = " ".join(career_issues)
        action_step = (
            "1. Implement a weekly 'Impact Log': write down 3 quantifiable wins every Friday.\n"
            "2. Stop taking workplace friction personally — practice structured, non-emotional documentation.\n"
            "3. Seek out an established senior mentor outside your immediate team."
        )
        vedic_remedy = (
            "1. Light an earthen mustard oil lamp (diya) under a Peepal tree on Saturday evenings.\n"
            "2. Offer fresh water to the Sun every morning facing East within 1 hour of sunrise.\n"
            "3. Avoid initiating major career showdowns during Tuesdays."
        )
        mantra = "Om Sham Shanaishcharaya Namaha (108 times on Saturday evenings) for career stability."
        charity = "Feed black sesame seeds or bread (roti) with mustard oil to stray dogs or workers on Saturdays."
        lucky_timing = "Saturday evenings for reflective planning; wear Navy Blue or Charcoal."

    remedies_by_stream["career"] = {
        "stream_name": "Career & Professional Growth",
        "status": career_status,
        "problem_detected": career_core_problem,
        "root_cause": f"Governed by 10th house lord {lord_10} in {p_10['sign_name']} (House {p_10['house']}) and Saturn in House {sat_p['house']}.",
        "actionable_habits": action_step,
        "vedic_remedy": vedic_remedy,
        "mantra_sound": mantra,
        "charity_karma_correction": charity,
        "optimal_day_and_color": lucky_timing
    }

    # =========================================================================
    # 2. MONEY & WEALTH STREAM (Artha)
    # =========================================================================
    lord_2 = h_lords[2]
    lord_11 = h_lords[11]
    p_2 = planets[lord_2]
    p_11 = planets[lord_11]
    jup_p = planets["Jupiter"]

    wealth_issues = []
    if p_2["house"] in [6, 8, 12] or p_2["dignity"] in ["Debilitated", "Enemy"]:
        wealth_issues.append(f"Lord of accumulated assets ({lord_2}) is under pressure in House {p_2['house']}, leading to cash leakage or unforeseen expenses.")
    if jup_p["dignity"] == "Debilitated" or jup_p["is_combust"]:
        wealth_issues.append("Jupiter's placement indicates money arrives but can slip through fingers via sudden expenditures.")

    # Check Kemadruma
    kemadruma = any(y["name"] == "Kemadruma Dosha" for y in yogas)
    if kemadruma:
        wealth_issues.append("Kemadruma influence can create psychological financial anxiety and periodic liquidity droughts.")

    if not wealth_issues:
        wealth_status = "Prosperous Flow"
        wealth_problem = "Occasional budgeting drift, but wealth generation capacity is sound."
        w_action = "Automate at least 20% of income directly into long-term compounding instruments on salary day."
        w_remedy = "Keep North-East quadrant of your home clean, uncluttered, and place a brass bowl with clean water there."
        w_mantra = "Om Shreem Hreem Kleem Shreem Laxmi Re-entry Namaha."
        w_charity = "Donate yellow lentils (chana dal) or turmeric to a community kitchen on Thursdays."
        w_timing = "Thursday mid-mornings, wear Golden Yellow or Saffron."
    else:
        wealth_status = "Attention Required"
        wealth_problem = " ".join(wealth_issues)
        w_action = (
            "1. Implement the '48-Hour Purchase Rule': Wait 2 days before any non-essential expense over $50.\n"
            "2. Establish an emergency liquid reserve fund strictly in a separate bank with no debit card access.\n"
            "3. Audit recurring subscriptions and renegotiate interest terms."
        )
        w_remedy = (
            "1. Avoid keeping broken glass, non-working clocks, or rusted iron at home.\n"
            "2. Offer a pinch of turmeric and yellow flowers to Lord Vishnu or Lakshmi on Thursdays.\n"
            "3. Feed green fodder or spinach to cows on Wednesday mornings."
        )
        w_mantra = "Om Gam Ganapataye Namaha (108 times daily before starting financial transactions)."
        w_charity = "Support an underprivileged child's school textbooks or stationery supplies."
        w_timing = "Wednesday & Thursday mornings; wear Pastel Yellow or Light Green."

    remedies_by_stream["wealth"] = {
        "stream_name": "Wealth & Asset Accumulation",
        "status": wealth_status,
        "problem_detected": wealth_problem,
        "root_cause": f"Assets governed by 2nd lord {lord_2} (House {p_2['house']}) and Jupiter ({jup_p['dignity']}).",
        "actionable_habits": w_action,
        "vedic_remedy": w_remedy,
        "mantra_sound": w_mantra,
        "charity_karma_correction": w_charity,
        "optimal_day_and_color": w_timing
    }

    # =========================================================================
    # 3. LOVE & MARRIAGE STREAM (Kama / Vivaha)
    # =========================================================================
    lord_7 = h_lords[7]
    p_7 = planets[lord_7]
    venus_p = planets["Venus"]
    mars_p = planets["Mars"]

    rel_issues = []
    # Check Mangal Dosha
    mangal_yoga = next((y for y in yogas if "Mangal Dosha" in y["name"]), None)
    if mangal_yoga and "Cancelled" not in mangal_yoga.get("description", ""):
        rel_issues.append("Mars placement creates intense temperamental spikes, blunt speech, and impatience during domestic disagreements.")
    if venus_p["dignity"] in ["Debilitated", "Enemy"] or venus_p["is_combust"]:
        rel_issues.append("Venus placement indicates feeling emotionally underappreciated or seeking perfectionism in partnerships.")
    if p_7["dignity"] == "Debilitated":
        rel_issues.append(f"7th house lord ({lord_7}) in debilitation signals tendency to attract partners with contrasting emotional rhythms.")

    if not rel_issues:
        rel_status = "Harmonious"
        rel_problem = "Mild occasional miscommunications; fundamentally aligned."
        r_action = "Practice active reflective listening: summarize what your partner said before responding."
        r_remedy = "Keep fresh white flowers in the bedroom on Friday mornings."
        r_mantra = "Om Shukraya Namaha (21 times on Friday mornings)."
        r_charity = "Donate white clothes or rice/sugar to an elderly woman on Fridays."
        r_timing = "Friday evenings, wear Soft White, Cream, or Rose Pink."
    else:
        rel_status = "Needs Conscious Care"
        rel_problem = " ".join(rel_issues)
        r_action = (
            "1. Practice the '3-Second Pause': When irritated, breathe deeply for 3 seconds before uttering words.\n"
            "2. Never bring past historical disputes into a current discussion.\n"
            "3. Dedicate 30 minutes of uninterrupted screen-free quality time weekly."
        )
        r_remedy = (
            "1. Recite Hanuman Chalisa every Tuesday evening to channel and soften excessive Martian heat.\n"
            "2. Carry or wear a small piece of pure silver (e.g. silver ring or pendant) to calm the emotional mind.\n"
            "3. Avoid arguments during Tuesday evenings."
        )
        r_mantra = "Om Kleem Krishnaya Namaha (for sweetening relationship bonds) or Hanuman Chalisa on Tuesdays."
        r_charity = "Donate sweet red sweets (jalebi or revdi) to children on Tuesdays."
        r_timing = "Tuesdays for calming Mars; Fridays for Venus. Wear Warm Rose, Cream, or Pastel Pink."

    remedies_by_stream["relationships"] = {
        "stream_name": "Love, Marriage & Partnerships",
        "status": rel_status,
        "problem_detected": rel_problem,
        "root_cause": f"7th house ruled by {lord_7} (in {p_7['sign_name']}) with Venus in {venus_p['sign_name']} and Mars in House {mars_p['house']}.",
        "actionable_habits": r_action,
        "vedic_remedy": r_remedy,
        "mantra_sound": r_mantra,
        "charity_karma_correction": r_charity,
        "optimal_day_and_color": r_timing
    }

    # =========================================================================
    # 4. HEALTH & PHYSICAL ENERGY STREAM (Arogya)
    # =========================================================================
    lord_1 = h_lords[1]
    p_1 = planets[lord_1]
    moon_p = planets["Moon"]

    health_issues = []
    if p_1["house"] in [6, 8, 12]:
        health_issues.append(f"Ascendant lord ({lord_1}) is located in Dusthana house {p_1['house']}, requiring extra attention to physical stamina and immunity.")
    if sun_p["dignity"] == "Debilitated":
        health_issues.append("Low solar vitality can trigger seasonal sluggishness, eyesight strain, or bone density vulnerabilities.")
    if moon_p["dignity"] == "Debilitated" or moon_p["is_combust"]:
        health_issues.append("Moon sensitivity points to psychosomatic digestive issues and sleep irregularities during high stress.")

    if not health_issues:
        health_status = "Strong & Resilient"
        health_problem = "Constitution is well-anchored; maintain baseline routine."
        h_action = "Maintain a steady sleep schedule (in bed before 11 PM) and 2.5L daily hydration."
        h_remedy = "Drink water stored overnight in a pure copper vessel first thing in the morning."
        h_mantra = "Om Namah Shivaya (peaceful breath rhythm meditation)."
        h_charity = "Offer fruits to sick or elderly individuals."
        h_timing = "Mondays & Sundays; wear White or Warm Ochre."
    else:
        health_status = "Vulnerable / Needs Routine"
        health_problem = " ".join(health_issues)
        h_action = (
            "1. Anchor circadian rhythm: Wake up at the same hour daily; get 10 mins direct sunlight in eyes.\n"
            "2. Avoid eating heavy meals post 8:30 PM to protect liver and digestion.\n"
            "3. Incorporate gentle 20-min daily walks or yogic stretching."
        )
        h_remedy = (
            "1. Practice 5 rounds of Anulom Vilom (alternate nostril breathing) every morning.\n"
            "2. Keep a Holy Basil (Tulsi) plant at home and water it with devotion.\n"
            "3. Fast or consume light fruits/khichdi on Mondays or Ekadashi."
        )
        h_mantra = "Maha Mrityunjaya Mantra (Om Tryambakam Yajamahe...) 11 times every morning for vital shielding."
        h_charity = "Donate medicines or first-aid supplies to a charitable clinic."
        h_timing = "Sunday & Monday mornings; wear Pure White, Saffron, or Earthy tones."

    remedies_by_stream["health"] = {
        "stream_name": "Health, Energy & Vitality",
        "status": health_status,
        "problem_detected": health_problem,
        "root_cause": f"Physical constitution anchored by Ascendant in {asc['sign_name']} and Lagna lord {lord_1} in House {p_1['house']}.",
        "actionable_habits": h_action,
        "vedic_remedy": h_remedy,
        "mantra_sound": h_mantra,
        "charity_karma_correction": h_charity,
        "optimal_day_and_color": h_timing
    }

    # =========================================================================
    # 5. MIND, STUDIES & INTELLECT STREAM (Buddhi)
    # =========================================================================
    lord_5 = h_lords[5]
    p_5 = planets[lord_5]
    merc_p = planets["Mercury"]

    mind_issues = []
    if merc_p["dignity"] in ["Debilitated", "Enemy"] or merc_p["is_combust"]:
        mind_issues.append("Mercury's condition points to brain fog, overthinking, and multitasking exhaustion.")
    if p_5["dignity"] == "Debilitated":
        mind_issues.append("5th lord in debilitation can scatter academic retention and creative execution.")

    if not mind_issues:
        mind_status = "Sharp & Focused"
        mind_problem = "High mental acuity; channel it into strategic learning."
        m_action = "Work in 45-minute deep-work focus sprints with zero notifications."
        m_remedy = "Water a green broad-leaf plant on Wednesday mornings."
        m_mantra = "Om Budhaya Namaha or Saraswati Vandana."
        m_charity = "Donate pens, notebooks, or stationery to underprivileged students on Wednesday."
        m_timing = "Wednesday mornings, wear Emerald Green or Mint."
    else:
        mind_status = "Scattered / Restless"
        mind_problem = " ".join(mind_issues)
        m_action = (
            "1. Digital Sunset: Turn off all social media and bright screens 45 minutes before sleep.\n"
            "2. 'Brain Dump Journaling': Write down top 3 priorities the night before to eliminate morning anxiety.\n"
            "3. Single-tasking discipline: Do one task at a time."
        )
        m_remedy = (
            "1. Chant Gayatri Mantra 9 times facing East before studying or key analytical work.\n"
            "2. Keep a small potted Jade or Tulsi plant on your work desk.\n"
            "3. Consume a pinch of fennel seeds (saunf) after meals for mental clarity."
        )
        m_mantra = "Om Aim Saraswatyai Namaha (for learning, speech, and intellectual breakthroughs)."
        m_charity = "Sponsor educational supplies or feed green vegetables to birds."
        m_timing = "Wednesday mornings; wear Mint Green or Forest Green."

    remedies_by_stream["intellect"] = {
        "stream_name": "Mind, Focus & Studies",
        "status": mind_status,
        "problem_detected": mind_problem,
        "root_cause": f"Cognitive stream governed by 5th lord {lord_5} and Mercury in {merc_p['sign_name']}.",
        "actionable_habits": m_action,
        "vedic_remedy": m_remedy,
        "mantra_sound": m_mantra,
        "charity_karma_correction": m_charity,
        "optimal_day_and_color": m_timing
    }

    # =========================================================================
    # 6. ACTIVE DASHA REMEDY (The Master Planetary Trigger)
    # =========================================================================
    active_maha = active_dasha.get("active_mahadasha", "Jupiter")
    active_antar = active_dasha.get("active_antardasha", "Venus")

    DASHA_REMEDIES = {
        "Sun": {
            "focus": "Cultivate leadership, integrity, father's respect, and sun salutations.",
            "remedy": "Offer water to sunrise daily; donate copper or wheat on Sundays.",
            "mantra": "Om Suryaya Namaha",
            "avoid": "Ego confrontations and late morning sleeping."
        },
        "Moon": {
            "focus": "Emotional hygiene, maternal bonding, hydration, and creative peace.",
            "remedy": "Drink water from silver glass; offer milk/water to Shiva on Mondays.",
            "mantra": "Om Somaya Namaha",
            "avoid": "Staying awake late into the night."
        },
        "Mars": {
            "focus": "Channeling high drive into physical exercise, real estate, and disciplined action.",
            "remedy": "Recite Hanuman Chalisa on Tuesdays; donate red lentils.",
            "mantra": "Om Angarakaya Namaha",
            "avoid": "Road rage, hasty verbal reactions, and spicy excessive food."
        },
        "Mercury": {
            "focus": "Communication, commercial acumen, technology mastery, and writing.",
            "remedy": "Feed green grass/spinach to cows on Wednesdays; support schooling.",
            "mantra": "Om Budhaya Namaha",
            "avoid": "Over-promising and superficial gossip."
        },
        "Jupiter": {
            "focus": "Higher wisdom, mentorship, dharmic conduct, and expanding financial vision.",
            "remedy": "Apply saffron/turmeric tilak on forehead; respect teachers and gurus.",
            "mantra": "Om Brihaspataye Namaha",
            "avoid": "Arrogance of knowledge and disdaining spiritual traditions."
        },
        "Venus": {
            "focus": "Refining aesthetics, harmonious partnerships, creative art, and luxury balance.",
            "remedy": "Donate white sweets, wear clean fragrant clothes, honor women in life.",
            "mantra": "Om Shukraya Namaha",
            "avoid": "Indulgent sensory burnout and financial vanity."
        },
        "Saturn": {
            "focus": "Patience, long-term architectural thinking, humility, service to workers.",
            "remedy": "Light mustard oil lamp under Peepal on Saturday; help laborers/helpers.",
            "mantra": "Om Sham Shanaishcharaya Namaha",
            "avoid": "Procrastination, cheating the weak, and clutter."
        },
        "Rahu": {
            "focus": "Unconventional innovation, foreign horizons, avoiding delusions or shortcuts.",
            "remedy": "Feed street dogs; avoid gambling/speculative frenzy; keep sandalwood fragrance.",
            "mantra": "Om Rahave Namaha or Durga Saptashati",
            "avoid": "Alcohol, smoke, and get-rich-quick temptations."
        },
        "Ketu": {
            "focus": "Spiritual introspection, detachment, research, coding, and meditation.",
            "remedy": "Feed multi-colored (spotted) dogs; donate warm blankets to the destitute.",
            "mantra": "Om Ketave Namaha or Ganesha Atharvashirsha",
            "avoid": "Cynicism, escapism, and sudden emotional withdrawal."
        }
    }

    dasha_info = DASHA_REMEDIES.get(active_maha, DASHA_REMEDIES["Jupiter"])

    remedies_by_stream["active_dasha"] = {
        "stream_name": f"Current Active Dasha ({active_maha} / {active_antar})",
        "status": "Major Life Catalyst",
        "problem_detected": f"Your life is currently under the primary command of {active_maha} Mahadasha and {active_antar} Antardasha.",
        "root_cause": f"{active_maha} activates the houses it owns and resides in your chart.",
        "actionable_habits": dasha_info["focus"],
        "vedic_remedy": dasha_info["remedy"],
        "mantra_sound": dasha_info["mantra"],
        "charity_karma_correction": f"Align with {active_maha}'s energy through service. What to avoid: {dasha_info['avoid']}",
        "optimal_day_and_color": f"Honor the day of {active_maha}."
    }

    return remedies_by_stream

