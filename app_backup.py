import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ThermoGuard AI",
    page_icon="🔥",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    model = joblib.load("thermoguard_model_no_frp.pkl")
    label_encoder = joblib.load("label_encoder_no_frp.pkl")
    feature_columns = joblib.load("feature_columns_no_frp.pkl")

    return model, label_encoder, feature_columns


model, label_encoder, feature_columns = load_model()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🔥 ThermoGuard AI")
st.subheader("AI-Based Fire Risk Prediction System")

st.write(
    "Predict wildfire risk using satellite and environmental "
    "features without FRP to avoid target leakage."
)

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("📍 Fire Risk Input")

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
        value=300.0
    )

    scan = st.number_input(
        "Scan",
        value=1.0
    )

with col2:
    track = st.number_input(
        "Track",
        value=1.0
    )

    acq_time = st.number_input(
        "Acquisition Time",
        value=1200
    )

    bright_t31 = st.number_input(
        "Brightness T31",
        value=300.0
    )

    confidence = st.selectbox(
        "Confidence",
        ["l", "n"]
    )

with col3:
    daynight = st.selectbox(
        "Day / Night",
        ["D", "N"]
    )

    month = st.number_input(
        "Month",
        min_value=1,
        max_value=12,
        value=6
    )

    day = st.number_input(
        "Day",
        min_value=1,
        max_value=31,
        value=15
    )

    hour = st.number_input(
        "Hour",
        min_value=0,
        max_value=23,
        value=12
    )

st.divider()

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if st.button("🔍 Predict Fire Risk", use_container_width=True):

    # Basic date calculations
    date = pd.Timestamp(year=2026, month=int(month), day=int(day))

    year = 2026
    day_of_year = date.dayofyear
    day_of_week = date.dayofweek
    week_of_year = int(date.isocalendar().week)
    minute = 0

    is_weekend = 1 if day_of_week >= 5 else 0

    # Seasonal calculation
    if month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8, 9]:
        season = "summer"
    else:
        season = "winter"

    # Cyclic features
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

    # --------------------------------------------------
    # CREATE INPUT DATA
    # --------------------------------------------------

    input_data = pd.DataFrame({
        "latitude": [latitude],
        "longitude": [longitude],
        "brightness": [brightness],
        "scan": [scan],
        "track": [track],
        "acq_time": [acq_time],
        "bright_t31": [bright_t31],
        "type": [0],
        "year": [year],
        "month": [month],
        "day": [day],
        "day_of_year": [day_of_year],
        "day_of_week": [day_of_week],
        "week_of_year": [week_of_year],
        "hour": [hour],
        "minute": [minute],
        "is_weekend": [is_weekend],
        "month_sin": [month_sin],
        "month_cos": [month_cos],
        "hour_sin": [hour_sin],
        "hour_cos": [hour_cos],
        "day_of_year_sin": [day_of_year_sin],
        "day_of_year_cos": [day_of_year_cos],
        "confidence": [confidence],
        "version": ["2.0NRT"],
        "daynight": [daynight],
        "season": [season]
    })

    # --------------------------------------------------
    # ENCODE CATEGORICAL FEATURES
    # --------------------------------------------------

    categorical_columns = input_data.select_dtypes(
        include=["object"]
    ).columns.tolist()

    input_data = pd.get_dummies(
        input_data,
        columns=categorical_columns,
        drop_first=True
    )

    input_data = input_data.replace(
        [np.inf, -np.inf],
        np.nan
    )

    input_data = input_data.fillna(0)

    # Match training features
    input_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    risk = label_encoder.inverse_transform(
        [prediction]
    )[0]

    confidence_score = max(probabilities) * 100

    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------

    st.divider()

    st.header("🎯 Prediction Result")

    if risk == "High":
        st.error("🔴 HIGH FIRE RISK")

    elif risk == "Medium":
        st.warning("🟠 MEDIUM FIRE RISK")

    else:
        st.success("🟢 LOW FIRE RISK")

    st.metric(
        "Prediction Confidence",
        f"{confidence_score:.2f}%"
    )

    st.subheader("Risk Probabilities")

    for class_number, probability in zip(
        model.classes_,
        probabilities
    ):
        class_name = label_encoder.inverse_transform(
            [class_number]
        )[0]

        st.write(
            f"**{class_name}**: "
            f"{probability * 100:.2f}%"
        )

        st.progress(
            float(probability)
        )

    st.divider()

    st.info(
        "ThermoGuard AI prediction is generated using "
        "the leakage-free Random Forest model."
    )