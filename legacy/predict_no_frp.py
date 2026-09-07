import pandas as pd
import numpy as np
import joblib

print("=" * 60)
print("THERMOGUARD AI - LEAKAGE-FREE FIRE RISK PREDICTION")
print("=" * 60)

# Load model
model = joblib.load("thermoguard_model_no_frp.pkl")
label_encoder = joblib.load("label_encoder_no_frp.pkl")
feature_columns = joblib.load("feature_columns_no_frp.pkl")

print("\nLoading dataset...")

df = pd.read_csv(
    "data_cleaned.csv",
    low_memory=False
)

print("Dataset loaded!")
print("Total rows:", len(df))

# Select row
row_number = int(
    input(f"\nEnter row number (0 - {len(df)-1}): ")
)

row = df.iloc[[row_number]].copy()

# Save actual risk only for comparison
actual_risk = row["risk_level"].iloc[0]

# Remove columns not used by model
drop_columns = [
    "risk_level",
    "frp",
    "acq_date",
    "datetime",
    "satellite",
    "instrument"
]

drop_columns = [
    col for col in drop_columns
    if col in row.columns
]

X = row.drop(columns=drop_columns)

# Encode categorical columns
categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

# Handle invalid values
X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

# Match training features
X = X.reindex(
    columns=feature_columns,
    fill_value=0
)

# Prediction
prediction = model.predict(X)[0]

probabilities = model.predict_proba(X)[0]

risk = label_encoder.inverse_transform(
    [prediction]
)[0]

confidence = max(probabilities) * 100

print("\n" + "=" * 60)
print("THERMOGUARD AI - PREDICTION RESULT")
print("=" * 60)

print("\nDataset Row     :", row_number)
print("Actual Risk     :", actual_risk)
print("Predicted Risk  :", risk)
print("Confidence      :", round(confidence, 2), "%")

print("\nClass Probabilities:")

for class_number, probability in zip(
    model.classes_,
    probabilities
):
    class_name = label_encoder.inverse_transform(
        [class_number]
    )[0]

    print(
        f"{class_name}: {probability * 100:.2f}%"
    )

print("\n" + "=" * 60)