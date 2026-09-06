ThermoGuard AI – ML Model Integration

Model: XGBoost Classifier
Model file: thermoguard_frp_model.pkl

Required files:
1. thermoguard_frp_model.pkl
2. label_encoder_frp.pkl
3. feature_columns_frp.pkl

Input features required by the model:

latitude
longitude
brightness
scan
track
acq_time
confidence
version
bright_t31
frp
daynight
type
year
month
day
day_of_year
day_of_week
week_of_year
hour
minute
is_weekend
season
month_sin
month_cos
hour_sin
hour_cos
day_of_year_sin
day_of_year_cos

The UI should collect the required inputs, perform the same preprocessing/encoding, pass the 28 features to the XGBoost model, and display the predicted risk level:
High / Low / Medium.

Label encoding:
0 = High
1 = Low
2 = Medium 