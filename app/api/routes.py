"""
FastAPI Route Handlers for Deterministic Horoscope API.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.schemas.horoscope_schemas import (
    BirthDetailsRequest, ChartResponse, PredictionResponse, DashaResponse, TransitResponse
)
from app.core.astronomy import (
    to_utc, calculate_julian_day, calculate_lahiri_ayanamsha,
    calculate_ascendant, calculate_all_planets
)
from app.core.houses import calculate_whole_sign_houses
from app.core.chart_engine import build_full_chart
from app.core.dasha_engine import calculate_vimshottari_dashas, get_active_dasha
from app.core.yoga_engine import detect_yogas
from app.core.transit_engine import evaluate_transits
from app.core.prediction_engine import synthesize_predictions
from app.core.remedies_engine import generate_stream_remedies
from app.core.geocoder import resolve_location
from app.db.database import db_manager

router = APIRouter(prefix="/api/horoscope", tags=["Horoscope Engine"])


@router.post("/calculate", response_model=ChartResponse)
def calculate_horoscope(payload: BirthDetailsRequest):
    """
    Computes a complete, mathematically exact Vedic natal chart (D1 & D9)
    from date, time, and geographic coordinates or city name.
    """
    try:
        # 1. Automatic Geolocation & Timezone Resolution
        latitude, longitude, timezone_str, place_display = resolve_location(
            payload.place_name, payload.latitude, payload.longitude, payload.birth_timezone
        )

        # 2. Coordinate & Ephemeris Normalization
        utc_dt = to_utc(payload.birth_date, payload.birth_time, timezone_str)
        jd = calculate_julian_day(utc_dt)
        ayanamsha = calculate_lahiri_ayanamsha(jd)

        # 3. Ascendant & Planetary Coordinates
        asc_meta = calculate_ascendant(jd, latitude, longitude, ayanamsha)
        raw_planets = calculate_all_planets(jd, ayanamsha)

        # 4. Bhavas (Whole Sign Houses) & D1/D9 Chart
        houses = calculate_whole_sign_houses(asc_meta["sidereal_ascendant"])
        full_chart = build_full_chart(raw_planets, asc_meta)

        # 5. Temporal Chronology (Vimshottari Dasha)
        moon_nak = full_chart["planets"]["Moon"]["nakshatra"]
        dashas = calculate_vimshottari_dashas(utc_dt, moon_nak)
        active_dasha = get_active_dasha(dashas, datetime.now(timezone.utc))

        # 6. Yogas & Doshas Detection
        yogas = detect_yogas(full_chart, houses)

        # 7. Domain Scoring & Problem Remedies
        predictions = synthesize_predictions(full_chart, houses, yogas, active_dasha)
        remedies = generate_stream_remedies(full_chart, houses, yogas, active_dasha)
        predictions["remedies"] = remedies

        # 8. Persist to Database
        user_meta_to_save = payload.model_dump()
        user_meta_to_save["latitude"] = latitude
        user_meta_to_save["longitude"] = longitude
        user_meta_to_save["birth_timezone"] = timezone_str
        user_meta_to_save["place_name"] = place_display

        chart_id = db_manager.save_full_record(
            user_meta=user_meta_to_save,
            chart=full_chart,
            houses=houses,
            jd=jd,
            ayanamsha=ayanamsha,
            dashas=dashas,
            yogas=yogas,
            predictions=predictions
        )

        return {
            "chart_id": chart_id,
            "user_name": payload.name,
            "birth_date": str(payload.birth_date),
            "birth_time": str(payload.birth_time),
            "timezone": timezone_str,
            "place_name": place_display,
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "julian_day": round(jd, 6),
            "ayanamsha": round(ayanamsha, 4),
            "ascendant": full_chart["ascendant"],
            "planets": full_chart["planets"],
            "houses": houses
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Astronomical calculation error: {str(e)}")


@router.get("/{chart_id}", response_model=ChartResponse)
def get_chart_by_id(chart_id: str):
    """Retrieves an existing natal chart by its unique ID."""
    record = db_manager.get_chart(chart_id)
    if not record:
        raise HTTPException(status_code=404, detail="Chart not found")

    return {
        "chart_id": record["chart_id"],
        "user_name": record["user_name"],
        "birth_date": record["birth_date"],
        "birth_time": record["birth_time"],
        "timezone": record["timezone"],
        "place_name": record["place_name"],
        "coordinates": record["coordinates"],
        "julian_day": round(record["julian_day"], 6),
        "ayanamsha": round(record["ayanamsha"], 4),
        "ascendant": record["chart"]["ascendant"],
        "planets": record["chart"]["planets"],
        "houses": record["houses"]
    }


@router.get("/{chart_id}/dasha", response_model=DashaResponse)
def get_chart_dashas(chart_id: str):
    """Retrieves the complete 120-year Vimshottari Dasha timeline and active period."""
    dashas = db_manager.get_dashas(chart_id)
    if not dashas:
        raise HTTPException(status_code=404, detail="Dasha records not found for chart")

    active_dasha = get_active_dasha(dashas, datetime.now(timezone.utc))
    return {
        "chart_id": chart_id,
        "active_dasha": active_dasha,
        "mahadashas": dashas
    }


@router.get("/{chart_id}/yogas")
def get_chart_yogas(chart_id: str):
    """Retrieves all classical yogas, doshas, and mitigations detected for this chart."""
    yogas = db_manager.get_yogas(chart_id)
    if yogas is None:
        raise HTTPException(status_code=404, detail="Yogas not found for chart")
    return {"chart_id": chart_id, "yogas_count": len(yogas), "yogas": yogas}


@router.get("/{chart_id}/predictions", response_model=PredictionResponse)
def get_chart_predictions(chart_id: str):
    """Retrieves domain ratings (0-100) and explainable predictions across 6 life pillars."""
    preds = db_manager.get_predictions(chart_id)
    if not preds:
        raise HTTPException(status_code=404, detail="Predictions not found for chart")
    return {
        "chart_id": chart_id,
        "domain_scores": preds["domain_scores"],
        "dasha_highlight": preds["dasha_highlight"],
        "readings": preds["readings"],
        "remedies": preds.get("remedies")
    }


@router.get("/{chart_id}/remedies")
def get_chart_remedies(chart_id: str):
    """Retrieves root-cause analysis and actionable step-by-step remedies for every life stream."""
    preds = db_manager.get_predictions(chart_id)
    if not preds or "remedies" not in preds:
        raise HTTPException(status_code=404, detail="Remedies not found for chart")
    return {"chart_id": chart_id, "remedies": preds["remedies"]}


@router.get("/{chart_id}/transits", response_model=TransitResponse)
def get_chart_transits(chart_id: str):
    """Computes real-time transits, Sade Sati status, and Jupiter Gochar."""
    record = db_manager.get_chart(chart_id)
    if not record:
        raise HTTPException(status_code=404, detail="Chart not found")

    moon_sign_id = record["chart"]["planets"]["Moon"]["sign_id"]
    asc_sign_id = record["chart"]["ascendant"]["sign_id"]

    transit_data = evaluate_transits(moon_sign_id, asc_sign_id, datetime.now(timezone.utc))
    return transit_data

