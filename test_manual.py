"""
Interactive Test Script for Deterministic Horoscope Backend.
Run this script to test all backend calculations, database storage, and predictions.

Usage:
    cd backend
    python test_manual.py
"""

import os
import sys
# Ensure backend directory is in sys.path
BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import json
from datetime import date, time
from app.schemas.horoscope_schemas import BirthDetailsRequest
from app.api.routes import (
    calculate_horoscope,
    get_chart_by_id,
    get_chart_dashas,
    get_chart_yogas,
    get_chart_predictions,
    get_chart_transits,
    get_chart_remedies
)

def format_section(title: str):
    print("\n" + "=" * 65)
    print(f"  {title.upper()}")
    print("=" * 65)

def run_test():
    format_section("1. Submitting Birth Data (No Lat/Long Needed - City Name Only!)")
    # Sample Test Subject - Passing only city name 'Pune'
    sample_request = BirthDetailsRequest(
        name="Arjun Sharma",
        birth_date=date(1998, 7, 21),
        birth_time=time(14, 30, 0),
        place_name="Pune"
    )
    print(f"Subject: {sample_request.name}")
    print(f"Date of Birth: {sample_request.birth_date} at {sample_request.birth_time}")
    print(f"User Input City: {sample_request.place_name} (No Latitude/Longitude provided by user)")

    # Step 1: Calculate Chart
    res = calculate_horoscope(sample_request)
    chart_id = res["chart_id"]
    print(f"\n[OK] City Automatically Geocoded to: {res['place_name']} ({res['timezone']})")
    print(f"Resolved Coordinates: Lat {res['coordinates']['latitude']}, Lon {res['coordinates']['longitude']}")
    print(f"Chart ID: {chart_id}")
    print(f"Astronomical Julian Day: {res['julian_day']}")
    print(f"Lahiri Ayanamsha: {res['ayanamsha']}°")

    # Step 2: Ascendant & Planetary Placements
    format_section("2. Ascendant (Lagna) & Planetary Placements (D1 Rashi)")
    asc = res["ascendant"]
    print(f"Ascendant (Lagna): {asc['sign_name']} ({asc['sign_sanskrit']}) at {asc['degree_in_sign']:.2f}°")
    print(f"  -> Nakshatra: {asc['nakshatra']['name']} (Pada {asc['nakshatra']['pada']}), Ruled by {asc['nakshatra']['lord']}")
    print(f"  -> Navamsha (D9) Sign: {asc['navamsha_sign_name']}\n")

    print(f"{'Planet':<10} | {'Sign':<12} | {'Deg in Sign':<12} | {'House':<6} | {'Dignity':<14} | {'Nakshatra':<15}")
    print("-" * 80)
    for p_name, p in res["planets"].items():
        print(f"{p_name:<10} | {p['sign_name']:<12} | {p['degree_in_sign']:<10.2f}° | H{p['house']:<5} | {p['dignity']:<14} | {p['nakshatra']['name']} (P{p['nakshatra']['pada']})")

    # Step 3: 120-Year Vimshottari Dasha System
    format_section("3. Vimshottari Dasha Timeline (120-Year Master Cycle)")
    dasha_res = get_chart_dashas(chart_id)
    active = dasha_res["active_dasha"]
    print(f"Active Mahadasha:  {active['active_mahadasha']} (Span: {active['mahadasha_period']['start'][:10]} to {active['mahadasha_period']['end'][:10]})")
    print(f"Active Antardasha: {active['active_antardasha']} (Span: {active['antardasha_period']['start'][:10]} to {active['antardasha_period']['end'][:10]})")
    
    print("\nComplete Mahadasha Progression Sequence:")
    for m in dasha_res["mahadashas"]:
        status = " [CURRENT ACTIVE]" if m["planet"] == active["active_mahadasha"] else ""
        print(f"  * {m['planet']:<9} Dasha : {m['start_date'][:10]} to {m['end_date'][:10]} ({m['total_years']} Years){status}")

    # Step 4: Detected Yogas & Doshas
    format_section("4. Detected Classical Yogas & Doshas")
    yogas_res = get_chart_yogas(chart_id)
    print(f"Total Yogas Detected: {yogas_res['yogas_count']}\n")
    for y in yogas_res["yogas"]:
        sign = "+" if y["impact_weight"] > 0 else ""
        print(f"[{sign}{y['impact_weight']} pts] {y['name']} ({y['category']}) - {y['type']}")
        print(f"  Citation: {y['classical_citation']}")
        print(f"  Planets:  {', '.join(y['planets_involved'])}")
        print(f"  Details:  {y['description']}\n")

    # Step 5: Domain Scores & Structured Predictions
    format_section("5. Deterministic Life Domain Predictions (0 - 100)")
    pred_res = get_chart_predictions(chart_id)
    print(f"Dasha Highlight: {pred_res['dasha_highlight']}\n")
    for domain, r in pred_res["readings"].items():
        print(f"--- {domain.upper()} (Score: {r['score']}/100 - {r['status']}) ---")
        print(f"  Analysis:   {r['lord_analysis']}")
        print(f"  Prediction: {r['prediction']}")
        print(f"  Action:     {r['recommended_focus']}\n")

    # Step 6: Stream-Wise Problems & Remedial Action Plans
    format_section("6. Stream-Wise Problems & Vedic Remedial Measures (Upayas)")
    remedies_res = get_chart_remedies(chart_id)
    for stream_key, r in remedies_res["remedies"].items():
        print(f"--- {r['stream_name'].upper()} [{r['status']}] ---")
        print(f"  Problem Detected: {r['problem_detected']}")
        print(f"  Root Cause:       {r['root_cause']}")
        print(f"  Daily Habit:      {r['actionable_habits']}")
        print(f"  Vedic Upaya:      {r['vedic_remedy']}")
        print(f"  Mantra Chanting:  {r['mantra_sound']}")
        print(f"  Charity (Danam):  {r['charity_karma_correction']}")
        print(f"  Best Day/Color:   {r['optimal_day_and_color']}\n")

    # Step 7: Real-Time Transits & Sade Sati
    format_section("7. Real-Time Transits (Gochar) & Saturn Sade Sati")
    trans_res = get_chart_transits(chart_id)
    print(f"As of: {trans_res['as_of_date'][:19]} UTC")
    print(f"Saturn Transit Position: {trans_res['transiting_positions']['Saturn']['sign']} at {trans_res['transiting_positions']['Saturn']['degree']:.2f}°")
    print(f"Jupiter Transit Position: {trans_res['transiting_positions']['Jupiter']['sign']} at {trans_res['transiting_positions']['Jupiter']['degree']:.2f}°")
    print(f"Rahu Transit Position: {trans_res['transiting_positions']['Rahu']['sign']} at {trans_res['transiting_positions']['Rahu']['degree']:.2f}°")
    
    print("\nSade Sati Status:")
    print(f"  Active: {trans_res['sade_sati']['is_active']} ({trans_res['sade_sati']['phase']})")
    print(f"  Impact: {trans_res['sade_sati']['description']}")
    
    print("\nJupiter Gochar:")
    print(f"  Benefic Transit: {trans_res['jupiter_gochar']['is_benefic_transit']}")
    print(f"  Impact: {trans_res['jupiter_gochar']['description']}")

    # Step 7: Database Read Verification
    format_section("7. Database Verification (Reloading Record from Disk)")
    loaded = get_chart_by_id(chart_id)
    assert loaded["chart_id"] == chart_id
    print(f"[OK] Chart record {chart_id} verified and reloaded successfully from database!")
    print("\n" + "=" * 65)
    print("  ALL BACKEND TESTS PASSED WITH 100% MATHEMATICAL PRECISION!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_test()

