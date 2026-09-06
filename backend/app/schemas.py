from datetime import date, time

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    latitude: float = 20.0
    longitude: float = 73.0
    brightness: float = 330.0
    scan: float = 1.0
    track: float = 1.0
    acq_time: int = Field(1200, ge=0, le=2359)
    confidence: str = "h"
    version: str = "2.0NRT"
    daynight: str = "D"
    fire_type: int = -1
    bright_t31: float = 310.0
    frp: float = Field(5.0, ge=0)
    observation_date: date
    observation_time: time


class RiskProbability(BaseModel):
    risk_level: str
    probability: float


class PredictResponse(BaseModel):
    predicted_risk: str
    confidence_score: float
    prediction_proba: list[RiskProbability]

    fire_source: str
    fire_source_confidence: float

    fire_detected: bool
    brightness_difference: float

    intensity: str
    intensity_message: str

    thermal_status: str
    thermal_message: str

    season: str

    latitude: float
    longitude: float
    brightness: float
    frp: float
    daynight: str
