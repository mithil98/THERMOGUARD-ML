from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from . import ml
from .report import create_pdf_report
from .schemas import PredictRequest, PredictResponse, RiskProbability

app = FastAPI(title="ThermoGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _run_prediction(req: PredictRequest) -> dict:
    if not ml.models_ready():
        raise HTTPException(status_code=503, detail=f"Risk model unavailable: {ml.load_error()}")

    result = ml.predict_fire(
        req.latitude,
        req.longitude,
        req.brightness,
        req.scan,
        req.track,
        req.acq_time,
        req.confidence,
        req.version,
        req.daynight,
        req.fire_type,
        req.bright_t31,
        req.frp,
        req.observation_date,
        req.observation_time,
    )

    fire_detected, brightness_difference = ml.detect_fire(req.brightness, req.bright_t31, req.frp)
    intensity, intensity_message = ml.classify_intensity(req.frp)
    thermal_status, thermal_message = ml.classify_thermal(brightness_difference)

    prediction_proba = [
        {"risk_level": str(level), "probability": round(float(p) * 100, 2)}
        for level, p in zip(ml.label_encoder.classes_, result["prediction_proba"])
    ]

    return {
        "predicted_risk": str(result["predicted_risk"]),
        "confidence_score": round(float(result["confidence_score"]), 2),
        "prediction_proba": prediction_proba,
        "fire_source": str(result["fire_source"]),
        "fire_source_confidence": round(float(result["fire_source_confidence"]), 2),
        "fire_detected": bool(fire_detected),
        "brightness_difference": round(float(brightness_difference), 2),
        "intensity": intensity,
        "intensity_message": intensity_message,
        "thermal_status": thermal_status,
        "thermal_message": thermal_message,
        "season": result["season"],
        "latitude": req.latitude,
        "longitude": req.longitude,
        "brightness": req.brightness,
        "frp": req.frp,
        "daynight": req.daynight,
    }


@app.get("/api/health")
def health():
    return {
        "risk_model_ready": ml.models_ready(),
        "fire_source_model_ready": ml.fire_source_model is not None,
        "error": ml.load_error(),
    }


@app.get("/api/meta")
def meta():
    if not ml.models_ready():
        raise HTTPException(status_code=503, detail=f"Risk model unavailable: {ml.load_error()}")

    importances = []
    if hasattr(ml.model, "feature_importances_"):
        pairs = sorted(
            zip(ml.feature_columns, ml.model.feature_importances_),
            key=lambda x: x[1],
            reverse=True,
        )
        importances = [{"feature": f, "importance": round(float(i), 6)} for f, i in pairs]

    return {
        "feature_columns": list(ml.feature_columns),
        "risk_classes": list(ml.label_encoder.classes_),
        "feature_importances": importances,
        "fire_source_available": ml.fire_source_model is not None,
        "performance": {
            # Static figures displayed by the original app.py (st.metric calls),
            # kept as-is for parity even though len(feature_columns) is actually 35.
            "model": "XGBoost",
            "features": 28,
            "test_samples": 126935,
            "accuracy": 99.92,
        },
    }


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    return _run_prediction(req)


@app.post("/api/report")
def report(req: PredictRequest):
    ctx = _run_prediction(req)
    ctx.update(
        {
            "scan": req.scan,
            "track": req.track,
            "acq_time": req.acq_time,
            "confidence": req.confidence,
            "version": req.version,
            "fire_type": req.fire_type,
            "bright_t31": req.bright_t31,
            "observation_date": req.observation_date,
            "observation_time": req.observation_time,
        }
    )

    pdf_buffer = create_pdf_report(ctx)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ThermoGuard_AI_Report.pdf"},
    )
