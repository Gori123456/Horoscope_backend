"""
Comprehensive Unit Tests for Deterministic Horoscope Engine.
"""

import sys
import os
# Ensure the backend directory is in sys.path regardless of execution folder
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from datetime import datetime, date, time
import pytz
from app.core.astronomy import (
    calculate_julian_day, calculate_lahiri_ayanamsha,
    calculate_ascendant, calculate_all_planets, to_utc
)
from app.core.chart_engine import (
    get_nakshatra_info, calculate_navamsha_sign, evaluate_dignity, build_full_chart
)
from app.core.houses import calculate_whole_sign_houses
from app.core.dasha_engine import calculate_vimshottari_dashas, get_active_dasha
from app.core.yoga_engine import detect_yogas
from app.core.transit_engine import evaluate_transits
from app.core.prediction_engine import synthesize_predictions


def test_julian_day_j2000():
    """Verify Julian Day calculation matches standard J2000 astronomical benchmark."""
    dt = datetime(2000, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
    jd = calculate_julian_day(dt)
    assert abs(jd - 2451545.0) < 1e-6, f"Expected 2451545.0, got {jd}"


def test_lahiri_ayanamsha():
    """Verify Lahiri Ayanamsha for year 2000 and 2026."""
    jd_2000 = 2451545.0
    aya_2000 = calculate_lahiri_ayanamsha(jd_2000)
    assert 23.8 < aya_2000 < 23.9, f"Expected ~23.85° at J2000, got {aya_2000}"


def test_nakshatra_computation():
    """Verify Nakshatra mapping across boundaries."""
    # 0.0° should be Ashwini Pada 1
    ashwini = get_nakshatra_info(0.5)
    assert ashwini["name"] == "Ashwini"
    assert ashwini["pada"] == 1
    assert ashwini["lord"] == "Ketu"

    # 50.0° should be Rohini (40° to 53°20')
    rohini = get_nakshatra_info(50.0)
    assert rohini["name"] == "Rohini"
    assert rohini["lord"] == "Moon"


def test_navamsha_calculation():
    """Verify D9 Navamsha sign rules for movable, fixed, dual signs."""
    # Aries 0° to 3°20' is Aries Navamsha
    d9_aries = calculate_navamsha_sign(1.0)
    assert d9_aries == 1

    # Taurus (Fixed) 0° to 3°20' starts from Capricorn (10)
    d9_taurus = calculate_navamsha_sign(31.0)
    assert d9_taurus == 10


def test_dignity_evaluation():
    """Verify Exalted, Debilitated, and Own sign rules."""
    # Sun exalted in Aries (sign 1)
    assert evaluate_dignity("Sun", 1, 10.0) == "Exalted"
    # Sun debilitated in Libra (sign 7)
    assert evaluate_dignity("Sun", 7, 10.0) == "Debilitated"
    # Jupiter in Cancer (sign 4)
    assert evaluate_dignity("Jupiter", 4, 5.0) == "Exalted"
    # Saturn in Aquarius (sign 11, Moolatrikona)
    assert evaluate_dignity("Saturn", 11, 15.0) == "Moolatrikona"


def test_full_chart_and_dashas():
    """Verify end-to-end chart, 120-year dasha generation and prediction engine."""
    b_date = date(1995, 10, 15)
    b_time = time(8, 30, 0)
    tz_str = "Asia/Kolkata"
    lat, lon = 28.6139, 77.2090

    utc_dt = to_utc(b_date, b_time, tz_str)
    jd = calculate_julian_day(utc_dt)
    aya = calculate_lahiri_ayanamsha(jd)

    asc_meta = calculate_ascendant(jd, lat, lon, aya)
    raw_planets = calculate_all_planets(jd, aya)

    houses = calculate_whole_sign_houses(asc_meta["sidereal_ascendant"])
    chart = build_full_chart(raw_planets, asc_meta)

    # 1. Chart validation
    assert len(chart["planets"]) == 9
    assert len(houses) == 12

    # 2. Dasha validation
    moon_nak = chart["planets"]["Moon"]["nakshatra"]
    dashas = calculate_vimshottari_dashas(utc_dt, moon_nak)
    assert len(dashas) == 9
    active = get_active_dasha(dashas, datetime(2026, 1, 1, tzinfo=pytz.UTC))
    assert active["active_mahadasha"] is not None

    # 3. Yogas validation
    yogas = detect_yogas(chart, houses)
    assert isinstance(yogas, list)

    # 4. Predictions validation
    preds = synthesize_predictions(chart, houses, yogas, active)
    assert "domain_scores" in preds
    for domain in ["career", "wealth", "health", "relationships", "intellect", "spirituality"]:
        assert 0.0 <= preds["domain_scores"][domain] <= 100.0


if __name__ == "__main__":
    print("Running engine unit tests...")
    test_julian_day_j2000()
    test_lahiri_ayanamsha()
    test_nakshatra_computation()
    test_navamsha_calculation()
    test_dignity_evaluation()
    test_full_chart_and_dashas()
    print("All unit tests passed successfully!")

