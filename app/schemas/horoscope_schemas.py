"""
Pydantic Schemas for Request & Response Data Validation.
"""

from datetime import date, time
from typing import Optional, Any
from pydantic import BaseModel, Field

class BirthDetailsRequest(BaseModel):
    name: str = Field(..., example="Arjun")
    birth_date: date = Field(..., example="1998-07-21")
    birth_time: time = Field(..., example="14:30:00")
    birth_timezone: Optional[str] = Field(default=None, example="Asia/Kolkata")
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0, example=28.6139)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0, example=77.2090)
    place_name: Optional[str] = Field(default="New Delhi, India", example="New Delhi, India")

class NakshatraMeta(BaseModel):
    nakshatra_id: int
    name: str
    lord: str
    deity: str
    gana: str
    pada: int
    degree_in_nakshatra: float
    nakshatra_fraction_elapsed: float

class AscendantDetail(BaseModel):
    longitude: float
    sign_id: int
    sign_name: str
    sign_sanskrit: str
    degree_in_sign: float
    nakshatra: NakshatraMeta
    navamsha_sign_id: int
    navamsha_sign_name: str

class PlanetDetail(BaseModel):
    name: str
    sanskrit: str
    sidereal_longitude: float
    sign_id: int
    sign_name: str
    sign_sanskrit: str
    degree_in_sign: float
    house: int
    nakshatra: NakshatraMeta
    dignity: str
    is_retrograde: bool
    is_combust: bool
    navamsha_sign_id: int
    navamsha_sign_name: str

class HouseDetail(BaseModel):
    house_number: int
    sign_id: int
    sign_name: str
    sign_sanskrit: str
    lord: str
    start_degree: float
    end_degree: float
    classifications: list[str]

class ChartResponse(BaseModel):
    chart_id: str
    user_name: str
    birth_date: str
    birth_time: str
    timezone: str
    place_name: Optional[str]
    coordinates: dict[str, float]
    julian_day: float
    ayanamsha: float
    ascendant: AscendantDetail
    planets: dict[str, PlanetDetail]
    houses: list[HouseDetail]

class YogaItem(BaseModel):
    name: str
    category: str
    type: str
    impact_weight: int
    classical_citation: str
    description: str
    planets_involved: list[str]

class DomainReading(BaseModel):
    score: float
    status: str
    lord_analysis: str
    prediction: str
    recommended_focus: str

class PredictionResponse(BaseModel):
    chart_id: str
    domain_scores: dict[str, float]
    dasha_highlight: str
    readings: dict[str, DomainReading]
    remedies: Optional[dict[str, Any]] = None

class DashaResponse(BaseModel):
    chart_id: str
    active_dasha: dict[str, Any]
    mahadashas: list[dict[str, Any]]

class TransitResponse(BaseModel):
    as_of_date: str
    transiting_positions: dict[str, Any]
    sade_sati: dict[str, Any]
    jupiter_gochar: dict[str, Any]

