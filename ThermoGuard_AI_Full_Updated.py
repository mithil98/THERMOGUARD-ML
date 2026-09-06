import streamlit as st
import pandas as pd
import numpy as np
import joblib

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
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

model = None
label_encoder = None
feature_columns = None

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
    fire_source_model = None
    fire_source_encoder = None
    fire_source_features = None


# ============================================================
# CUSTOM CSS - IMPROVED VISIBILITY
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117 !important;
    color: #f8fafc !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

p, span, div { line-height: 1.6 !important; }

.title {
    font-size: 46px !important;
    font-weight: 800 !important;
    text-align: center !important;
    color: #ff4b4b !important;
    margin-bottom: 10px !important;
    line-height: 1.3 !important;
}

.subtitle {
    text-align: center !important;
    font-size: 20px !important;
    font-weight: 500 !important;
    color: #e5e7eb !important;
    margin-bottom: 35px !important;
    line-height: 1.6 !important;
}

.section-title {
    font-size: 28px !important;
    font-weight: 750 !important;
    color: #ffffff !important;
    margin-top: 30px !important;
    margin-bottom: 20px !important;
    line-height: 1.5 !important;
}

label {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 650 !important;
    line-height: 1.5 !important;
}

.stNumberInput input {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 500 !important;
    min-height: 46px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    min-height: 46px !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #111827 !important;
    font-size: 16px !important;
}

.stDateInput input,
.stTimeInput input {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-size: 16px !important;
    min-height: 46px !important;
}

.stButton > button {
    width: 100% !important;
    min-height: 58px !important;
    font-size: 19px !important;
    font-weight: 750 !important;
    border-radius: 12px !important;
    margin-top: 18px !important;
}

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    min-height: 125px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}

[data-testid="stMetricLabel"] {
    color: #374151 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    line-height: 1.5 !important;
    white-space: normal !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    line-height: 1.4 !important;
    white-space: normal !important;
}

.risk-high, .risk-medium, .risk-low {
    width: 100% !important;
    min-height: 170px !important;
    box-sizing: border-box !important;
    overflow: visible !important;
    padding: 28px !important;
    border-radius: 16px !important;
    text-align: center !important;
    margin: 20px 0 25px 0 !important;
}

.risk-high {
    background-color: #ffe5e5 !important;
    border: 3px solid #d62828 !important;
}
.risk-high h1 {
    color: #c1121f !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    margin-bottom: 12px !important;
}
.risk-high h3 {
    color: #1f2937 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}
.risk-high p {
    color: #374151 !important;
    font-size: 18px !important;
}

.risk-medium {
    background-color: #fff3d6 !important;
    border: 3px solid #f4a261 !important;
}
.risk-medium h1 {
    color: #d96b00 !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    margin-bottom: 12px !important;
}
.risk-medium h3 {
    color: #1f2937 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}
.risk-medium p {
    color: #374151 !important;
    font-size: 18px !important;
}

.risk-low {
    background-color: #e2f7e9 !important;
    border: 3px solid #2a9d8f !important;
}
.risk-low h1 {
    color: #16805c !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    margin-bottom: 12px !important;
}
.risk-low h3 {
    color: #1f2937 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}
.risk-low p {
    color: #374151 !important;
    font-size: 18px !important;
}

.info-box {
    background-color: #eaf4ff !important;
    border-left: 7px solid #2196f3 !important;
    padding: 24px !important;
    border-radius: 12px !important;
    margin: 20px 0 !important;
    color: #111827 !important;
    font-size: 17px !important;
    line-height: 1.8 !important;
}
.info-box b {
    color: #0f4c81 !important;
    font-size: 21px !important;
}

.alert-box {
    background-color: #fff3cd !important;
    border-left: 7px solid #ff9800 !important;
    padding: 24px !important;
    border-radius: 12px !important;
    margin: 20px 0 !important;
    color: #1f2937 !important;
    font-size: 17px !important;
    line-height: 1.8 !important;
}
.alert-box h3 {
    color: #9a4d00 !important;
    font-size: 23px !important;
    font-weight: 800 !important;
}

.stAlert {
    font-size: 17px !important;
    line-height: 1.7 !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

[data-testid="stDataFrame"] {
    width: 100% !important;
    max-width: 100% !important;
    margin-top: 12px !important;
    margin-bottom: 30px !important;
    font-size: 16px !important;
}
[data-testid="stDataFrame"] * {
    font-size: 16px !important;
}

[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"],
[data-testid="stChart"] {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 350px !important;
    margin-top: 20px !important;
    margin-bottom: 35px !important;
}

[data-testid="stExpander"] {
    border-radius: 12px !important;
    margin-top: 15px !important;
    margin-bottom: 15px !important;
}
[data-testid="stExpander"] summary {
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}
section[data-testid="stSidebar"] * {
    color: #1f2937 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #111827 !important;
    font-size: 22px !important;
    font-weight: 750 !important;
}
section[data-testid="stSidebar"] p {
    color: #374151 !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
}

p {
    color: #e5e7eb !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    line-height: 1.5 !important;
}

.stDownloadButton > button {
    width: 100% !important;
    min-height: 55px !important;
    font-size: 18px !important;
    font-weight: 750 !important;
    border-radius: 12px !important;
}

.footer {
    text-align: center !important;
    color: #d1d5db !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
    padding: 25px !important;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .title { font-size: 34px !important; }
    .subtitle { font-size: 17px !important; }
    .section-title { font-size: 24px !important; }
    [data-testid="stMetric"] {
        min-height: 115px !important;
        padding: 16px !important;
    }
    [data-testid="stMetricValue"] { font-size: 22px !important; }
    .risk-high h1,
    .risk-medium h1,
    .risk-low h1 { font-size: 30px !important; }
}



/* ============================================================
   FORCE TEXT VISIBILITY FIX - FINAL OVERRIDE
============================================================ */

.stApp,
.stApp * {
    opacity: 1 !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stText"],
.stApp p,
.stApp span {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stWidgetLabel"] label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label,
.stTimeInput label {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-testid="stDataFrame"] * {
    color: #111111 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

[data-testid="stMetric"] * {
    opacity: 1 !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p {
    color: #111827 !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #000000 !important;
    font-size: 28px !important;
    font-weight: 900 !important;
    opacity: 1 !important;
}

.info-box,
.info-box *,
.alert-box,
.alert-box * {
    opacity: 1 !important;
}

.info-box,
.info-box p,
.info-box span,
.info-box div,
.alert-box,
.alert-box p,
.alert-box span,
.alert-box div {
    color: #111111 !important;
}

.info-box,
.alert-box {
    font-size: 18px !important;
    font-weight: 600 !important;
}

[data-testid="stAlert"] {
    opacity: 1 !important;
}

[data-testid="stAlert"] *,
.stAlert * {
    color: #111111 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #ffffff !important;
    font-size: 19px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

[data-testid="stExpander"] p,
[data-testid="stExpander"] span {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #111111 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] p {
    font-size: 17px !important;
    font-weight: 600 !important;
}

.stButton button,
.stButton button * {
    color: #ffffff !important;
    font-size: 19px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

.footer,
.footer * {
    color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

.stCaption,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #ffffff !important;
    opacity: 1 !important;
}

hr {
    border-color: #64748b !important;
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)



# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🔥 ThermoGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Based Wildfire Risk Prediction & Fire Source Analysis System</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🔥 ThermoGuard AI")

    st.write(
        "ThermoGuard AI analyzes satellite hotspot and "
        "environmental information to estimate fire risk."
    )

    st.divider()

    st.subheader("System Pipeline")

    st.write("🛰️ Satellite Hotspot")
    st.write("⬇️")
    st.write("🔥 Fire Source Analysis")
    st.write("⬇️")
    st.write("📊 Risk Assessment")
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


# ============================================================
# COLUMN 1
# ============================================================

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


# ============================================================
# COLUMN 2
# ============================================================

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


# ============================================================
# COLUMN 3
# ============================================================

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
# PREDICTION BUTTON
# ============================================================

predict_button = st.button(
    "🔥 ANALYZE FIRE RISK",
    use_container_width=True,
    type="primary"
)


# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    # ========================================================
    # DATE / TIME FEATURES
    # ========================================================

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


    # ========================================================
    # SEASON
    # ========================================================

    if month in [12, 1, 2]:
        season = "winter"

    elif month in [3, 4, 5]:
        season = "spring"

    elif month in [6, 7, 8, 9]:
        season = "summer"

    else:
        season = "autumn"


    # ========================================================
    # CATEGORICAL MAPPINGS
    # ========================================================

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


    # ========================================================
    # CYCLIC FEATURES
    # ========================================================

    month_sin = np.sin(
        2 * np.pi * month / 12
    )

    month_cos = np.cos(
        2 * np.pi * month / 12
    )

    hour_sin = np.sin(
        2 * np.pi * hour / 24
    )

    hour_cos = np.cos(
        2 * np.pi * hour / 24
    )

    day_of_year_sin = np.sin(
        2 * np.pi * day_of_year / 365
    )

    day_of_year_cos = np.cos(
        2 * np.pi * day_of_year / 365
    )


    # ========================================================
    # BUILD INPUT DATA
    # ========================================================

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


    # ========================================================
    # RISK MODEL PREDICTION
    # ========================================================

    try:

        input_risk_data = input_data.reindex(
            columns=feature_columns,
            fill_value=0
        )

        input_risk_data = input_risk_data.apply(
            pd.to_numeric,
            errors="coerce"
        ).fillna(0)

        prediction = model.predict(
            input_risk_data
        )

        prediction_proba = model.predict_proba(
            input_risk_data
        )[0]

        predicted_class = prediction[0]

        predicted_risk = label_encoder.inverse_transform(
            [predicted_class]
        )[0]

        confidence_score = (
            np.max(prediction_proba) * 100
        )

    except Exception as e:

        st.error("Risk prediction failed.")
        st.error(str(e))
        st.stop()


    # ========================================================
    # FIRE SOURCE PREDICTION
    # ========================================================

    fire_source = "Not Available"
    fire_source_confidence = 0.0

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

            fire_source = (
                fire_source_encoder.inverse_transform(
                    source_prediction
                )[0]
            )

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

        except Exception as e:

            fire_source = "Prediction Error"

            st.warning(
                "Fire source prediction failed: "
                + str(e)
            )


    # ========================================================
    # RESULT SECTION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">🔥 Prediction Result</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # RISK DISPLAY
    # ========================================================

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
    # SOURCE INFORMATION
    # ========================================================

    st.markdown(
        '<div class="section-title">🔥 Fire Source Analysis</div>',
        unsafe_allow_html=True
    )

    source_descriptions = {

        "Vegetation Fire":
            "The hotspot is classified as a presumed vegetation fire.",

        "Other Land Source":
            "The hotspot is classified as another static land source.",

        "Offshore":
            "The hotspot is classified as an offshore hotspot.",

        "Unknown":
            "The hotspot source could not be determined.",

        "Not Available":
            "Fire source model is not available.",

        "Prediction Error":
            "Fire source prediction could not be completed."
    }

    st.info(
        source_descriptions.get(
            fire_source,
            "Fire source classification completed."
        )
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

    industrial_like = (
        fire_source == "Other Land Source"
    )

    high_risk = (
        str(predicted_risk).lower() == "high"
    )


    if industrial_like and high_risk:

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

    elif industrial_like:

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

        "Risk Level":
            label_encoder.classes_,

        "Probability (%)":
            prediction_proba * 100

    })

    probability_df["Probability (%)"] = (
        probability_df["Probability (%)"].round(2)
    )


    # Probability table

    st.dataframe(
        probability_df,
        use_container_width=True,
        hide_index=True
    )


    # Probability chart

    st.markdown(
        "#### 📊 Risk Probability Distribution"
    )

    st.bar_chart(
        probability_df.set_index(
            "Risk Level"
        ),
        use_container_width=True
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
        use_container_width=True,
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


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

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
        # RISK
        # ----------------------------------------------------

        risk_data = [

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
            colWidths=[180, 300]
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
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ])
        )

        elements.append(
            risk_table
        )

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

        elements.append(
            input_table
        )

        elements.append(
            Spacer(1, 20)
        )


        # ----------------------------------------------------
        # PROBABILITIES
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
        # MODEL INFORMATION
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                "Model Information",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                "Risk Model: XGBoost",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                "Risk Model Features: 28",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                "Fire Source Model: XGBoost",
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
                "The current dataset does not contain direct "
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


        # ----------------------------------------------------
        # BUILD PDF
        # ----------------------------------------------------

        doc.build(elements)

        buffer.seek(0)

        return buffer


    # ========================================================
    # PDF DOWNLOAD BUTTON
    # ========================================================

    pdf_file = create_pdf_report()

    st.download_button(

        label="📄 Download PDF Report",

        data=pdf_file,

        file_name="ThermoGuard_AI_Report.pdf",

        mime="application/pdf",

        use_container_width=True
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
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            importance_df.set_index(
                "Feature"
            ).head(15),
            use_container_width=True
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
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🔥 <b>ThermoGuard AI</b><br>
        AI-Based Wildfire Risk Prediction System<br>
        Satellite Hotspot → Source Analysis → Risk Assessment
        → Alert → Map → Report
    </div>
    """,
    unsafe_allow_html=True
)