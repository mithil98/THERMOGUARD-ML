import streamlit as st
import pandas as pd
import numpy as np
import joblib

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
from io import BytesIO


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ThermoGuard AI",
    page_icon="🔥",
    layout="wide"
)


# ============================================================
# MODEL FILES
# ============================================================

MODEL_FILE = "thermoguard_best.pkl"
ENCODER_FILE = "label_encoder_best.pkl"
FEATURE_FILE = "feature_columns_best.pkl"

FIRE_SOURCE_MODEL_FILE = "thermoguard_fire_source_model.pkl"
FIRE_SOURCE_ENCODER_FILE = "fire_source_label_encoder.pkl"
FIRE_SOURCE_FEATURE_FILE = "fire_source_features.pkl"


# ============================================================
# LOAD RISK MODEL
# ============================================================

try:
    model = joblib.load(MODEL_FILE)
    label_encoder = joblib.load(ENCODER_FILE)
    feature_columns = joblib.load(FEATURE_FILE)

except Exception as e:
    st.error("Risk model files could not be loaded.")
    st.error(str(e))
    st.stop()


# ============================================================
# LOAD FIRE SOURCE MODEL
# ============================================================

fire_source_model = None
fire_source_encoder = None
fire_source_features = None

try:
    fire_source_model = joblib.load(FIRE_SOURCE_MODEL_FILE)
    fire_source_encoder = joblib.load(FIRE_SOURCE_ENCODER_FILE)
    fire_source_features = joblib.load(FIRE_SOURCE_FEATURE_FILE)

except Exception:
    pass


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff !important;
    color: #111827 !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

p, span, li, div {
    line-height: 1.6 !important;
}

.stApp p,
.stApp span,
.stApp li {
    color: #111827 !important;
    font-size: 17px !important;
}

.title {
    font-size: 46px !important;
    font-weight: 900 !important;
    text-align: center !important;
    color: #d62828 !important;
    margin-bottom: 10px !important;
}

.subtitle {
    text-align: center !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #475569 !important;
    margin-bottom: 35px !important;
}

.section-title {
    font-size: 30px !important;
    font-weight: 900 !important;
    color: #111827 !important;
    margin-top: 30px !important;
    margin-bottom: 20px !important;
}

label {
    color: #111827 !important;
    font-size: 17px !important;
    font-weight: 750 !important;
}

.stNumberInput input,
.stTextInput input,
.stDateInput input,
.stTimeInput input {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-size: 16px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #111827 !important;
}

.stButton > button {
    width: 100% !important;
    min-height: 58px !important;
    font-size: 19px !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
}

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    min-height: 125px !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-size: 16px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 28px !important;
    font-weight: 900 !important;
}

.risk-high,
.risk-medium,
.risk-low {
    width: 100% !important;
    min-height: 175px !important;
    box-sizing: border-box !important;
    overflow: visible !important;
    padding: 30px !important;
    border-radius: 16px !important;
    text-align: center !important;
    margin: 20px 0 25px 0 !important;
}

.risk-high {
    background-color: #ffe5e5 !important;
    border: 3px solid #d62828 !important;
}

.risk-medium {
    background-color: #fff3d6 !important;
    border: 3px solid #f4a261 !important;
}

.risk-low {
    background-color: #e2f7e9 !important;
    border: 3px solid #2a9d8f !important;
}

.risk-high h1,
.risk-medium h1,
.risk-low h1 {
    font-size: 38px !important;
    font-weight: 900 !important;
}

.risk-high h3,
.risk-medium h3,
.risk-low h3 {
    color: #111827 !important;
    font-size: 23px !important;
    font-weight: 800 !important;
}

.risk-high p,
.risk-medium p,
.risk-low p {
    color: #111827 !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

.risk-high h1 {
    color: #b91c1c !important;
}

.risk-medium h1 {
    color: #b45309 !important;
}

.risk-low h1 {
    color: #047857 !important;
}

.info-box {
    background-color: #eaf4ff !important;
    border-left: 7px solid #2196f3 !important;
    padding: 24px !important;
    border-radius: 12px !important;
    margin: 20px 0 !important;
    color: #111827 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}

.alert-box {
    background-color: #fff3cd !important;
    border-left: 7px solid #ff9800 !important;
    padding: 24px !important;
    border-radius: 12px !important;
    margin: 20px 0 !important;
    color: #111827 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}

.live-box {
    background-color: #f8fafc !important;
    border: 2px solid #94a3b8 !important;
    border-radius: 16px !important;
    padding: 25px !important;
    margin: 20px 0 !important;
}

.analysis-card {
    background-color: #f8fafc !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 14px !important;
    padding: 22px !important;
    margin-bottom: 18px !important;
    min-height: 140px !important;
}

.analysis-card h3 {
    color: #111827 !important;
    font-size: 20px !important;
    font-weight: 800 !important;
}

.analysis-card p {
    color: #374151 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

.footer {
    text-align: center !important;
    color: #334155 !important;
    font-size: 16px !important;
    padding: 25px !important;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

hr {
    border-color: #cbd5e1 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# BUILD FEATURES
# ============================================================

def build_input_data(
    latitude,
    longitude,
    brightness,
    scan,
    track,
    acq_time,
    confidence,
    version,
    daynight,
    fire_type,
    bright_t31,
    frp,
    observation_date,
    observation_time
):

    obs_datetime = datetime.combine(
        observation_date,
        observation_time
    )

    year = obs_datetime.year
    month = obs_datetime.month
    day = obs_datetime.day

    day_of_year = obs_datetime.timetuple().tm_yday
    day_of_week = obs_datetime.weekday()
    week_of_year = int(obs_datetime.strftime("%V"))

    hour = obs_datetime.hour
    minute = obs_datetime.minute

    is_weekend = 1 if day_of_week >= 5 else 0

    if month in [12, 1, 2]:
        season = "winter"
    elif month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8, 9]:
        season = "summer"
    else:
        season = "autumn"

    confidence_mapping = {
        "h": 0,
        "l": 1,
        "n": 2
    }

    version_mapping = {
        "2.0NRT": 0
    }

    daynight_mapping = {
        "D": 0,
        "N": 1
    }

    season_mapping = {
        "autumn": 0,
        "spring": 1,
        "summer": 2,
        "winter": 3
    }

    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)

    hour_sin = np.sin(2 * np.pi * hour / 24)
    hour_cos = np.cos(2 * np.pi * hour / 24)

    day_of_year_sin = np.sin(
        2 * np.pi * day_of_year / 365
    )

    day_of_year_cos = np.cos(
        2 * np.pi * day_of_year / 365
    )

    input_data = pd.DataFrame([{

        "latitude": latitude,
        "longitude": longitude,
        "brightness": brightness,
        "scan": scan,
        "track": track,
        "acq_time": acq_time,

        "confidence": confidence_mapping[confidence],
        "version": version_mapping[version],

        "bright_t31": bright_t31,
        "frp": frp,

        "daynight": daynight_mapping[daynight],
        "type": fire_type,

        "year": year,
        "month": month,
        "day": day,

        "day_of_year": day_of_year,
        "day_of_week": day_of_week,
        "week_of_year": week_of_year,

        "hour": hour,
        "minute": minute,

        "is_weekend": is_weekend,

        "season": season_mapping[season],

        "month_sin": month_sin,
        "month_cos": month_cos,

        "hour_sin": hour_sin,
        "hour_cos": hour_cos,

        "day_of_year_sin": day_of_year_sin,
        "day_of_year_cos": day_of_year_cos

    }])

    return input_data, season


# ============================================================
# PRELIMINARY FIRE DETECTION
# ============================================================

def detect_fire(brightness, bright_t31, frp):

    brightness_difference = brightness - bright_t31

    # Preliminary transparent thermal screening
    fire_detected = (
        frp >= 2.40
        and brightness_difference >= 15
    )

    return fire_detected, brightness_difference


# ============================================================
# MODEL PREDICTION
# ============================================================

def predict_fire(
    latitude,
    longitude,
    brightness,
    scan,
    track,
    acq_time,
    confidence,
    version,
    daynight,
    fire_type,
    bright_t31,
    frp,
    observation_date,
    observation_time
):

    input_data, season = build_input_data(
        latitude,
        longitude,
        brightness,
        scan,
        track,
        acq_time,
        confidence,
        version,
        daynight,
        fire_type,
        bright_t31,
        frp,
        observation_date,
        observation_time
    )

    input_risk_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    input_risk_data = input_risk_data.apply(
        pd.to_numeric,
        errors="coerce"
    ).fillna(0)

    prediction = model.predict(input_risk_data)

    prediction_proba = model.predict_proba(
        input_risk_data
    )[0]

    predicted_class = prediction[0]

    predicted_risk = label_encoder.inverse_transform(
        [predicted_class]
    )[0]

    confidence_score = np.max(
        prediction_proba
    ) * 100

    fire_source = "Not Available"
    fire_source_confidence = 0.0
    source_probability = None

    if (
        fire_source_model is not None
        and fire_source_encoder is not None
        and fire_source_features is not None
    ):

        try:

            source_input = input_data.reindex(
                columns=fire_source_features,
                fill_value=0
            )

            source_input = source_input.apply(
                pd.to_numeric,
                errors="coerce"
            ).fillna(0)

            source_prediction = fire_source_model.predict(
                source_input
            )

            fire_source = fire_source_encoder.inverse_transform(
                source_prediction
            )[0]

            if hasattr(
                fire_source_model,
                "predict_proba"
            ):

                source_probability = (
                    fire_source_model.predict_proba(
                        source_input
                    )[0]
                )

                fire_source_confidence = (
                    np.max(source_probability) * 100
                )

        except Exception:

            fire_source = "Prediction Error"

    return {
        "input_data": input_data,
        "season": season,
        "predicted_risk": predicted_risk,
        "prediction_proba": prediction_proba,
        "confidence_score": confidence_score,
        "fire_source": fire_source,
        "fire_source_confidence": fire_source_confidence,
        "source_probability": source_probability
    }


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🔥 ThermoGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Based Wildfire Risk Prediction & Fire Source Analysis System'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🔥 ThermoGuard AI")

    st.write(
        "ThermoGuard AI analyzes satellite hotspot "
        "and environmental information to estimate "
        "wildfire risk."
    )

    st.divider()

    st.subheader("System Pipeline")

    st.write("🛰️ Satellite Hotspot")
    st.write("⬇️")
    st.write("🔥 Is it a Fire?")
    st.write("⬇️")
    st.write("🔥 Fire Source Analysis")
    st.write("⬇️")
    st.write("📊 Risk Assessment")
    st.write("⬇️")
    st.write("🔴 Live Interaction")
    st.write("⬇️")
    st.write("🚨 Alert System")
    st.write("⬇️")
    st.write("🗺️ Fire Map")
    st.write("⬇️")
    st.write("📄 PDF Report")


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📍 Fire Risk Input</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    latitude = st.number_input(
        "Latitude",
        value=20.0,
        format="%.6f"
    )

    longitude = st.number_input(
        "Longitude",
        value=73.0,
        format="%.6f"
    )

    brightness = st.number_input(
        "Brightness",
        value=330.0,
        format="%.2f"
    )

    scan = st.number_input(
        "Scan",
        value=1.0,
        format="%.2f"
    )

    track = st.number_input(
        "Track",
        value=1.0,
        format="%.2f"
    )


with col2:

    acq_time = st.number_input(
        "Acquisition Time",
        min_value=0,
        max_value=2359,
        value=1200,
        step=1
    )

    confidence = st.selectbox(
        "Confidence",
        ["h", "l", "n"]
    )

    version = st.selectbox(
        "Satellite Version",
        ["2.0NRT"]
    )

    daynight = st.selectbox(
        "Day / Night",
        ["D", "N"]
    )

    fire_type = st.selectbox(
        "Fire / Hotspot Type",
        [-1, 0, 2, 3]
    )


with col3:

    bright_t31 = st.number_input(
        "Brightness T31",
        value=310.0,
        format="%.2f"
    )

    frp = st.number_input(
        "FRP",
        min_value=0.0,
        value=5.0,
        format="%.2f"
    )

    observation_date = st.date_input(
        "Observation Date",
        value=datetime.now().date()
    )

    observation_time = st.time_input(
        "Observation Time",
        value=datetime.now().time()
    )


# ============================================================
# LIVE INTERACTION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔴 Live Fire Risk Interaction</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="live-box">
    <b>🎛️ Interactive Fire Simulation</b><br><br>
    Adjust the satellite fire parameters below.
    The AI model will immediately recalculate the
    fire risk and probability.
    </div>
    """,
    unsafe_allow_html=True
)

live_col1, live_col2 = st.columns(2)


with live_col1:

    live_brightness = st.slider(
        "🔥 Live Brightness",
        min_value=250.0,
        max_value=450.0,
        value=float(np.clip(brightness, 250, 450)),
        step=1.0
    )

    live_frp = st.slider(
        "⚡ Live FRP",
        min_value=0.0,
        max_value=100.0,
        value=float(np.clip(frp, 0, 100)),
        step=0.5
    )


with live_col2:

    live_bright_t31 = st.slider(
        "🌡️ Live Brightness T31",
        min_value=250.0,
        max_value=400.0,
        value=float(np.clip(bright_t31, 250, 400)),
        step=1.0
    )

    live_confidence = st.selectbox(
        "📡 Live Satellite Confidence",
        ["h", "l", "n"]
    )


# ============================================================
# LIVE PREDICTION
# ============================================================

try:

    live_result = predict_fire(
        latitude,
        longitude,
        live_brightness,
        scan,
        track,
        acq_time,
        live_confidence,
        version,
        daynight,
        fire_type,
        live_bright_t31,
        live_frp,
        observation_date,
        observation_time
    )

    live_risk = live_result["predicted_risk"]
    live_conf_score = live_result["confidence_score"]

    if str(live_risk).lower() == "high":

        st.markdown(
            f"""
            <div class="risk-high">
                <h1>🔴 LIVE HIGH RISK</h1>
                <h3>{live_risk}</h3>
                <p>Live AI Confidence: {live_conf_score:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif str(live_risk).lower() == "medium":

        st.markdown(
            f"""
            <div class="risk-medium">
                <h1>🟠 LIVE MEDIUM RISK</h1>
                <h3>{live_risk}</h3>
                <p>Live AI Confidence: {live_conf_score:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="risk-low">
                <h1>🟢 LIVE LOW RISK</h1>
                <h3>{live_risk}</h3>
                <p>Live AI Confidence: {live_conf_score:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    live_m1, live_m2, live_m3 = st.columns(3)

    with live_m1:
        st.metric(
            "Live Risk Confidence",
            f"{live_conf_score:.2f}%"
        )

    with live_m2:
        st.metric(
            "Live Brightness",
            f"{live_brightness:.1f}"
        )

    with live_m3:
        st.metric(
            "Live FRP",
            f"{live_frp:.1f}"
        )

    live_probability_df = pd.DataFrame({

        "Risk Level": label_encoder.classes_,

        "Probability (%)":
            live_result["prediction_proba"] * 100

    })

    live_probability_df["Probability (%)"] = (
        live_probability_df["Probability (%)"].round(2)
    )

    st.markdown("#### 📊 Live Risk Probability")

    st.bar_chart(
        live_probability_df.set_index("Risk Level"),
        width="stretch"
    )

except Exception as e:

    st.warning(
        "Live interaction prediction could not be calculated."
    )

    st.warning(str(e))


# ============================================================
# LIVE FIRE DETECTION
# ============================================================

live_fire_detected, live_brightness_difference = detect_fire(
    live_brightness,
    live_bright_t31,
    live_frp
)

st.divider()

st.markdown(
    '<div class="section-title">🔥 Fire Detection</div>',
    unsafe_allow_html=True
)

if live_fire_detected:

    st.markdown(
        f"""
        <div class="risk-high">

            <h1>🔥 FIRE DETECTED: YES</h1>

            <h3>Preliminary Thermal Hotspot Detection</h3>

            <p>
            Thermal hotspot indicators meet the
            preliminary fire-screening threshold.
            </p>

            <p>
            <b>FRP:</b> {live_frp:.2f}
            &nbsp;&nbsp; | &nbsp;&nbsp;
            <b>Brightness Difference:</b>
            {live_brightness_difference:.2f}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="risk-low">

            <h1>🟢 FIRE DETECTED: NO</h1>

            <h3>No Strong Thermal Fire Signature</h3>

            <p>
            The provided thermal hotspot indicators
            do not meet the preliminary fire-screening
            threshold.
            </p>

            <p>
            <b>FRP:</b> {live_frp:.2f}
            &nbsp;&nbsp; | &nbsp;&nbsp;
            <b>Brightness Difference:</b>
            {live_brightness_difference:.2f}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

st.info(
    "⚠️ Fire Detection is a preliminary rule-based "
    "thermal hotspot screening. It is not a separately "
    "trained binary Fire/No-Fire ML classifier."
)


# ============================================================
# MAIN PREDICTION BUTTON
# ============================================================

st.divider()

predict_button = st.button(
    "🔥 ANALYZE FIRE RISK",
    width="stretch",
    type="primary"
)


# ============================================================
# MAIN PREDICTION
# ============================================================

if predict_button:

    try:

        result = predict_fire(
            latitude,
            longitude,
            brightness,
            scan,
            track,
            acq_time,
            confidence,
            version,
            daynight,
            fire_type,
            bright_t31,
            frp,
            observation_date,
            observation_time
        )

        predicted_risk = result["predicted_risk"]
        prediction_proba = result["prediction_proba"]
        confidence_score = result["confidence_score"]

        fire_source = result["fire_source"]
        fire_source_confidence = result["fire_source_confidence"]

        season = result["season"]

        fire_detected, brightness_difference = detect_fire(
            brightness,
            bright_t31,
            frp
        )

    except Exception as e:

        st.error("Risk prediction failed.")
        st.error(str(e))
        st.stop()


# ========================================================
# FIRE SOURCE ANALYSIS
# ========================================================

st.markdown(
    '<div class="section-title">🔥 Fire Source Analysis</div>',
    unsafe_allow_html=True
)

source_descriptions = {
    "Vegetation Fire":
        "🌳 Vegetation-related fire hotspot detected.",

    "Other Land Source":
        "🏞️ Land-based thermal hotspot detected.",

    "Offshore":
        "🌊 Offshore thermal hotspot detected.",

    "Unknown":
        "❓ Fire source could not be determined confidently.",

    "Not Available":
        "⚠️ Fire source model is not available.",

    "Prediction Error":
        "⚠️ Fire source prediction could not be completed."
}

st.info(
    source_descriptions.get(
        fire_source,
        "Fire source classification completed."
    )
)

source_col1, source_col2 = st.columns(2)

with source_col1:

    st.metric(
        "🔥 Detected Fire Source",
        str(fire_source)
    )

with source_col2:

    st.metric(
        "📊 Source Confidence",
        f"{fire_source_confidence:.2f}%"
    )


# ========================================================
# SOURCE INTERPRETATION
# ========================================================

st.markdown("### 🔎 Source Interpretation")

if fire_source == "Vegetation Fire":

    st.success(
        "🌳 The hotspot is classified as a Vegetation Fire. "
        "It may involve forest, grassland or agricultural "
        "vegetation. The current dataset does not separate "
        "these categories."
    )

elif fire_source == "Other Land Source":

    st.warning(
        "🏞️ The hotspot is classified as Other Land Source. "
        "This should NOT be treated as a confirmed Industrial "
        "fire because the current dataset does not contain "
        "a direct Industrial label."
    )

elif fire_source == "Offshore":

    st.info(
        "🌊 The hotspot is classified as Offshore. "
        "Geographic verification is recommended."
    )

elif fire_source == "Unknown":

    st.warning(
        "❓ The fire source is Unknown. "
        "Additional satellite or geographic information "
        "is required."
    )

else:

    st.info(
        "ℹ️ Fire source analysis completed."
    )


    # ========================================================
    # PREDICTION RESULT
    # ========================================================

    st.markdown(
        '<div class="section-title">🔥 Prediction Result</div>',
        unsafe_allow_html=True
    )

    if str(predicted_risk).lower() == "high":

        st.markdown(
            f"""
            <div class="risk-high">
                <h1>🔴 HIGH RISK</h1>
                <h3>{predicted_risk}</h3>
                <p>Immediate attention is recommended.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif str(predicted_risk).lower() == "medium":

        st.markdown(
            f"""
            <div class="risk-medium">
                <h1>🟠 MEDIUM RISK</h1>
                <h3>{predicted_risk}</h3>
                <p>Monitoring is recommended.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="risk-low">
                <h1>🟢 LOW RISK</h1>
                <h3>{predicted_risk}</h3>
                <p>No immediate high-risk condition detected.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # CONFIDENCE + SOURCE
    # ========================================================

    col_a, col_b, col_c = st.columns(3)

    with col_a:

        st.metric(
            "Risk Confidence",
            f"{confidence_score:.2f}%"
        )

    with col_b:

        st.metric(
            "Detected Hotspot Source",
            fire_source
        )

    with col_c:

        st.metric(
            "Source Confidence",
            f"{fire_source_confidence:.2f}%"
        )


    # ========================================================
    # FIRE SOURCE ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-title">🔥 Fire Source Analysis</div>',
        unsafe_allow_html=True
    )

    source_descriptions = {

        "Vegetation Fire":
            "🌳 The hotspot is classified as a Vegetation Fire. "
            "This may represent burning vegetation, grassland, "
            "forest or other vegetated areas.",

        "Other Land Source":
            "🏞️ The hotspot is classified as an Other Land Source. "
            "This represents a land-based hotspot that is not "
            "directly labelled as vegetation, offshore or unknown.",

        "Offshore":
            "🌊 The hotspot is classified as Offshore. "
            "The detected thermal hotspot is associated with "
            "an offshore or water-related location.",

        "Unknown":
            "❓ The hotspot source is Unknown. "
            "The available satellite information is insufficient "
            "to determine the source.",

        "Not Available":
            "⚠️ Fire source model is not available.",

        "Prediction Error":
            "⚠️ Fire source prediction could not be completed."
    }

    st.info(
        source_descriptions.get(
            fire_source,
            "Fire source classification completed."
        )
    )


    # ========================================================
    # SOURCE INTERPRETATION
    # ========================================================

    st.markdown("### 🔎 Source Interpretation")

    if fire_source == "Vegetation Fire":

        st.success(
            "🌳 Vegetation-related hotspot detected. "
            "Forest, grassland or agricultural vegetation may "
            "be involved. The current dataset does not "
            "distinguish these categories."
        )

    elif fire_source == "Other Land Source":

        st.warning(
            "🏞️ Land-based hotspot detected. "
            "The dataset does not provide a direct Industrial "
            "label, so this category must NOT be treated as "
            "confirmed industrial fire."
        )

    elif fire_source == "Offshore":

        st.info(
            "🌊 Offshore hotspot detected. "
            "The location should be checked against geographic "
            "information for further verification."
        )

    elif fire_source == "Unknown":

        st.warning(
            "❓ Fire source is unknown. "
            "Additional satellite or geographic information "
            "is required."
        )


    source_col1, source_col2 = st.columns(2)

    with source_col1:

        st.metric(
            "🔥 Detected Source",
            str(fire_source)
        )

    with source_col2:

        st.metric(
            "📊 Source Confidence",
            f"{fire_source_confidence:.2f}%"
        )


    # ========================================================
    # FIRE ANALYSIS DASHBOARD
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Fire Analysis Dashboard</div>',
        unsafe_allow_html=True
    )

    analysis_col1, analysis_col2, analysis_col3, analysis_col4 = (
        st.columns(4)
    )

    with analysis_col1:

        st.metric(
            "🔥 Brightness",
            f"{brightness:.2f}"
        )

    with analysis_col2:

        st.metric(
            "⚡ FRP",
            f"{frp:.2f}"
        )

    with analysis_col3:

        st.metric(
            "🌡️ Brightness Difference",
            f"{brightness_difference:.2f}"
        )

    with analysis_col4:

        st.metric(
            "☀️ Day / Night",
            daynight
        )


    # ========================================================
    # FIRE INTENSITY
    # ========================================================

    st.markdown("### 🔥 Fire Intensity Analysis")

    if frp >= 10:

        intensity = "Very High"

        intensity_message = (
            "Very high fire radiative power detected. "
            "The hotspot may represent a strong thermal event."
        )

    elif frp >= 4.97:

        intensity = "High"

        intensity_message = (
            "High FRP detected. Increased fire activity "
            "should be monitored."
        )

    elif frp >= 2.40:

        intensity = "Medium"

        intensity_message = (
            "Medium FRP detected. Continued monitoring "
            "is recommended."
        )

    else:

        intensity = "Low"

        intensity_message = (
            "Low FRP detected. No strong thermal intensity "
            "is indicated by FRP alone."
        )

    st.markdown(
        f"""
        <div class="analysis-card">
        <h3>⚡ Fire Intensity: {intensity}</h3>
        <p>{intensity_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # THERMAL ANALYSIS
    # ========================================================

    st.markdown("### 🌡️ Thermal Analysis")

    if brightness_difference >= 30:

        thermal_status = "Strong Thermal Anomaly"

        thermal_message = (
            "Brightness is substantially higher than "
            "Brightness T31, indicating a strong thermal anomaly."
        )

    elif brightness_difference >= 15:

        thermal_status = "Moderate Thermal Anomaly"

        thermal_message = (
            "A moderate thermal difference is observed "
            "between brightness and Brightness T31."
        )

    else:

        thermal_status = "Low Thermal Difference"

        thermal_message = (
            "The difference between brightness and "
            "Brightness T31 is relatively small."
        )

    st.markdown(
        f"""
        <div class="analysis-card">
        <h3>🌡️ {thermal_status}</h3>
        <p>{thermal_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TEMPORAL ANALYSIS
    # ========================================================

    st.markdown("### 🕒 Temporal Analysis")

    if daynight == "D":

        temporal_message = (
            "The hotspot was observed during daytime. "
            "Daytime satellite observations may be affected "
            "by solar and surface conditions."
        )

    else:

        temporal_message = (
            "The hotspot was observed during nighttime. "
            "Nighttime thermal observations can provide "
            "useful hotspot information."
        )

    st.markdown(
        f"""
        <div class="analysis-card">
        <h3>
        🕒 Observation Period:
        {"Daytime" if daynight == "D" else "Nighttime"}
        </h3>
        <p>{temporal_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # LOCATION ANALYSIS
    # ========================================================

    st.markdown("### 📍 Location Analysis")

    st.markdown(
        f"""
        <div class="analysis-card">

        <h3>📍 Hotspot Location</h3>

        <p>
        Latitude: <b>{latitude:.6f}</b><br>
        Longitude: <b>{longitude:.6f}</b><br>
        Observation Season: <b>{season}</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # AI RISK INTERPRETATION
    # ========================================================

    st.markdown("### 🚨 AI Risk Interpretation")

    if str(predicted_risk).lower() == "high":

        interpretation = (
            "The AI model indicates a high-risk condition. "
            "The hotspot should be reviewed and monitored "
            "with priority."
        )

    elif str(predicted_risk).lower() == "medium":

        interpretation = (
            "The AI model indicates a medium-risk condition. "
            "Continued monitoring and verification are recommended."
        )

    else:

        interpretation = (
            "The AI model indicates a low-risk condition "
            "under the provided input parameters."
        )

    st.markdown(
        f"""
        <div class="alert-box">

        <b>🤖 AI Interpretation</b><br><br>

        {interpretation}

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # DATASET LIMITATION
    # ========================================================

    st.markdown(
        """
        <div class="info-box">

        <b>⚠️ Dataset Limitation</b><br><br>

        The current NASA hotspot dataset does not directly provide
        Forest / Agriculture / Industrial labels.<br><br>

        The current source analysis therefore uses hotspot source
        categories such as Vegetation Fire, Other Land Source,
        Offshore and Unknown.<br><br>

        A separate labelled dataset is required for genuine
        Forest / Agriculture / Industrial classification.

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ALERT ASSESSMENT
    # ========================================================

    st.markdown(
        '<div class="section-title">🚨 Alert Assessment</div>',
        unsafe_allow_html=True
    )

    land_source = (
        fire_source == "Other Land Source"
    )

    high_risk = (
        str(predicted_risk).lower() == "high"
    )

    if land_source and high_risk:

        st.markdown(
            """
            <div class="alert-box">

            <h3>🚨 HIGH PRIORITY ALERT</h3>

            The detected hotspot is classified as
            <b>Other Land Source</b> and the predicted
            fire risk is <b>HIGH</b>.<br><br>

            Immediate verification and monitoring are recommended.

            </div>
            """,
            unsafe_allow_html=True
        )

    elif high_risk:

        st.warning(
            "⚠️ HIGH fire risk detected. "
            "Immediate monitoring is recommended."
        )

    elif land_source:

        st.info(
            "ℹ️ Other Land Source detected. "
            "Additional verification is recommended."
        )

    else:

        st.success(
            "✅ No high-priority alert condition detected."
        )


    # ========================================================
    # RISK PROBABILITIES
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Risk Probabilities</div>',
        unsafe_allow_html=True
    )

    probability_df = pd.DataFrame({

        "Risk Level": label_encoder.classes_,

        "Probability (%)":
            prediction_proba * 100

    })

    probability_df["Probability (%)"] = (
        probability_df["Probability (%)"].round(2)
    )

    st.dataframe(
        probability_df,
        width="stretch",
        hide_index=True
    )

    st.markdown(
        "#### 📊 Risk Probability Distribution"
    )

    st.bar_chart(
        probability_df.set_index("Risk Level"),
        width="stretch"
    )


    # ========================================================
    # INPUT SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section-title">📋 Input Summary</div>',
        unsafe_allow_html=True
    )

    summary_df = pd.DataFrame({

        "Parameter": [

            "Latitude",
            "Longitude",
            "Brightness",
            "Scan",
            "Track",
            "Acquisition Time",
            "Brightness T31",
            "FRP",
            "Confidence",
            "Day / Night",
            "Hotspot Type",
            "Satellite Version",
            "Observation Date",
            "Observation Time",
            "Season"

        ],

        "Value": [

            latitude,
            longitude,
            brightness,
            scan,
            track,
            acq_time,
            bright_t31,
            frp,
            confidence,
            daynight,
            fire_type,
            version,
            str(observation_date),
            str(observation_time),
            season

        ]

    })

    st.dataframe(
        summary_df,
        width="stretch",
        hide_index=True
    )


    # ========================================================
    # INTERACTIVE FIRE MAP
    # ========================================================

    st.markdown(
        '<div class="section-title">🗺️ Fire Location Map</div>',
        unsafe_allow_html=True
    )

    map_df = pd.DataFrame({

        "latitude": [latitude],
        "longitude": [longitude]

    })

    st.map(map_df)


    # ========================================================
    # FRP WARNING
    # ========================================================

    if frp >= 4.97:

        st.warning(
            "🔥 High FRP detected. "
            "The current risk label is strongly influenced by FRP "
            "in the existing dataset/model."
        )

    elif frp >= 2.40:

        st.info(
            "🟠 Medium FRP range detected."
        )

    else:

        st.success(
            "🟢 Low FRP range detected."
        )


    # ========================================================
    # PDF REPORT
    # ========================================================

    def create_pdf_report():

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        title_style = styles["Title"]
        title_style.alignment = TA_CENTER

        elements = []

        elements.append(
            Paragraph(
                "ThermoGuard AI",
                title_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                "Wildfire Risk & Fire Source Analysis Report",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )


        # ----------------------------------------------------
        # FIRE DETECTION + RISK SUMMARY
        # ----------------------------------------------------

        risk_data = [

            [
                "Fire Detected",
                "YES" if fire_detected else "NO"
            ],

            [
                "Detection Method",
                "Preliminary Rule-Based Thermal Screening"
            ],

            [
                "Brightness Difference",
                f"{brightness_difference:.2f}"
            ],

            [
                "Risk Level",
                str(predicted_risk)
            ],

            [
                "Risk Confidence",
                f"{confidence_score:.2f}%"
            ],

            [
                "Fire Source",
                str(fire_source)
            ],

            [
                "Source Confidence",
                f"{fire_source_confidence:.2f}%"
            ],

            [
                "Fire Intensity",
                intensity
            ],

            [
                "Brightness",
                str(brightness)
            ],

            [
                "FRP",
                str(frp)
            ],

            [
                "Observation Date",
                str(observation_date)
            ],

            [
                "Observation Time",
                str(observation_time)
            ]

        ]


        risk_table = Table(
            risk_data,
            colWidths=[200, 280]
        )

        risk_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ])
        )

        elements.append(risk_table)

        elements.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # INPUT PARAMETERS
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "Input Parameters",
                styles["Heading2"]
            )
        )

        input_pdf_data = [

            ["Parameter", "Value"],

            ["Latitude", str(latitude)],
            ["Longitude", str(longitude)],
            ["Brightness", str(brightness)],
            ["Scan", str(scan)],
            ["Track", str(track)],
            ["Acquisition Time", str(acq_time)],
            ["Brightness T31", str(bright_t31)],
            ["FRP", str(frp)],
            ["Confidence", str(confidence)],
            ["Day / Night", str(daynight)],
            ["Hotspot Type", str(fire_type)],
            ["Satellite Version", str(version)],
            ["Observation Date", str(observation_date)],
            ["Observation Time", str(observation_time)],
            ["Season", str(season)]

        ]

        input_table = Table(
            input_pdf_data,
            colWidths=[220, 260]
        )

        input_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ])
        )

        elements.append(input_table)

        elements.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # RISK PROBABILITIES
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "Risk Probabilities",
                styles["Heading2"]
            )
        )

        probability_pdf_data = [
            ["Risk Level", "Probability"]
        ]

        for risk, probability in zip(
            label_encoder.classes_,
            prediction_proba
        ):

            probability_pdf_data.append(
                [
                    str(risk),
                    f"{probability * 100:.2f}%"
                ]
            )

        probability_table = Table(
            probability_pdf_data,
            colWidths=[220, 260]
        )

        probability_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ])
        )

        elements.append(
            probability_table
        )

        elements.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # FIRE ANALYSIS
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "Fire Analysis",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"Fire Detection: "
                f"{'YES' if fire_detected else 'NO'}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Brightness Difference: "
                f"{brightness_difference:.2f}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Fire Intensity: {intensity}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Thermal Status: {thermal_status}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Observation Period: "
                f"{'Daytime' if daynight == 'D' else 'Nighttime'}",
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )


        # ----------------------------------------------------
        # LIMITATION
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "<b>Important Limitation:</b> "
                "Fire Detection is a preliminary rule-based "
                "thermal hotspot screening and is not a separately "
                "trained binary Fire/No-Fire ML classifier. "
                "The current dataset also does not contain direct "
                "Forest / Agriculture / Industrial labels. "
                "Fire source categories are based on hotspot "
                "source classes available in the dataset.",
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                "Generated by ThermoGuard AI",
                styles["BodyText"]
            )
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer


    # ========================================================
    # PDF DOWNLOAD
    # ========================================================

    pdf_file = create_pdf_report()

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="ThermoGuard_AI_Report.pdf",
        mime="application/pdf",
        width="stretch"
    )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Model Performance</div>',
    unsafe_allow_html=True
)

perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

with perf_col1:

    st.metric(
        "Model",
        "XGBoost"
    )

with perf_col2:

    st.metric(
        "Features",
        "28"
    )

with perf_col3:

    st.metric(
        "Test Samples",
        "126,935"
    )

with perf_col4:

    st.metric(
        "Reported Accuracy",
        "99.92%"
    )


# ============================================================
# MODEL INFORMATION
# ============================================================

with st.expander("ℹ️ Model Information"):

    st.write(
        """
        **ThermoGuard AI Risk Model**

        Algorithm: XGBoost Classifier

        Features: 28

        Classes:
        - Low
        - Medium
        - High

        The model uses satellite hotspot and temporal
        environmental features.

        ⚠️ Important:

        The current dataset's risk labels are strongly related
        to FRP, so the reported 99.92% accuracy should not be
        interpreted as independent real-world wildfire prediction
        accuracy.
        """
    )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

with st.expander("📊 Feature Importance"):

    try:

        importance_df = pd.DataFrame({

            "Feature": feature_columns,

            "Importance": model.feature_importances_

        }).sort_values(
            "Importance",
            ascending=False
        )

        st.dataframe(
            importance_df,
            width="stretch",
            hide_index=True
        )

        st.bar_chart(
            importance_df.set_index(
                "Feature"
            ).head(15),
            width="stretch"
        )

    except Exception:

        st.warning(
            "Feature importance could not be displayed."
        )


# ============================================================
# FIRE SOURCE MODEL INFORMATION
# ============================================================

with st.expander("🔥 Fire Source Model Information"):

    if fire_source_model is not None:

        st.write(
            """
            **Fire Source Model**

            Algorithm: XGBoost Classifier

            Current source categories:

            - Vegetation Fire
            - Other Land Source
            - Offshore
            - Unknown

            ⚠️ This is not yet a Forest /
            Agriculture / Industrial classifier.

            A dedicated labelled dataset is required
            for those categories.
            """
        )

    else:

        st.warning(
            "Fire Source model files are not available."
        )


# ============================================================
# FIRE DETECTION INFORMATION
# ============================================================

with st.expander("🔥 Fire Detection Information"):

    st.write(
        """
        **Preliminary Fire Detection**

        The Fire Detection stage performs a transparent
        rule-based thermal hotspot screening before risk
        and source analysis.

        Screening indicators:

        - FRP ≥ 2.40
        - Brightness Difference ≥ 15

        When both conditions are satisfied:

        🔥 FIRE DETECTED: YES

        Otherwise:

        🟢 FIRE DETECTED: NO

        ⚠️ Important:

        This is NOT a separately trained binary
        Fire / No-Fire machine learning classifier.

        A genuine binary ML classifier would require
        a labelled dataset containing both confirmed
        fire and confirmed non-fire observations.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        🔥 <b>ThermoGuard AI</b><br>

        AI-Based Wildfire Risk Prediction System<br><br>

        Satellite Hotspot → Fire Detection →
        Source Analysis → Risk Assessment →
        Fire Analysis → Alert → Map → Report

    </div>
    """,
    unsafe_allow_html=True
)