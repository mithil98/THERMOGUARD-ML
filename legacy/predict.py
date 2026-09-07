import pandas as pd
import numpy as np
import joblib

# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 60)
print("THERMOGUARD AI - FIRE RISK PREDICTION")
print("=" * 60)

model = joblib.load("thermoguard_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(
    "data_cleaned.csv",
    low_memory=False
)

print("Dataset loaded!")
print("Total rows:", len(df))

# ============================================================
# SELECT A REAL DATASET ROW
# ============================================================

row_number = int(
    input(f"\nEnter row number (0 - {len(df)-1}): ")
)

row = df.iloc[[row_number]].copy()

# ============================================================
# SAME PREPROCESSING AS TRAINING
# ============================================================

drop_columns = [
    "risk_level",
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

# Categorical encoding
categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

# Replace infinite values
X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

# Fill missing values
X = X.fillna(0)

# ============================================================
# MATCH TRAINING FEATURES
# ============================================================

X = X.reindex(
    columns=feature_columns,
    fill_value=0
)

# ============================================================
# PREDICTION
# ============================================================

prediction = model.predict(X)[0]

probabilities = model.predict_proba(X)[0]

risk = label_encoder.inverse_transform(
    [prediction]
)[0]

confidence = max(probabilities) * 100

# ============================================================
# RESULT
# ============================================================

print("\n" + "=" * 60)
print("THERMOGUARD AI - PREDICTION RESULT")
print("=" * 60)

print("\nDataset Row       :", row_number)

print("Actual Risk       :", row["risk_level"].iloc[0])

print("Predicted Class   :", prediction)

print("Predicted Risk    :", risk)

print("Confidence        :", round(confidence, 2), "%")

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