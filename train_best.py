import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

print("Loading dataset...")

df = pd.read_csv("data_cleaned.csv", low_memory=False)

# -----------------------------
# Target
# -----------------------------
y = df["risk_level"]

# -----------------------------
# Feature engineering
# -----------------------------

df["brightness_diff"] = df["brightness"] - df["bright_t31"]
df["brightness_ratio"] = df["brightness"] / (df["bright_t31"] + 1)
df["scan_track_mean"] = (df["scan"] + df["track"]) / 2
df["scan_track_diff"] = abs(df["scan"] - df["track"])

df["hour_sin2"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos2"] = np.cos(2 * np.pi * df["hour"] / 24)

df["month_sin2"] = np.sin(2 * np.pi * df["month"] / 12)
df["month_cos2"] = np.cos(2 * np.pi * df["month"] / 12)

# -----------------------------
# Remove leakage / target columns
# -----------------------------
drop_columns = [
    "risk_level",
    "frp",
    "acq_date",
    "datetime",
    "satellite",
    "instrument"
]

X = df.drop(columns=drop_columns, errors="ignore")

# -----------------------------
# Encode categorical columns
# -----------------------------
categorical_columns = [
    "confidence",
    "version",
    "daynight",
    "season"
]

for col in categorical_columns:
    if col in X.columns:
        X[col] = pd.Categorical(X[col]).codes

# -----------------------------
# Clean data
# -----------------------------
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)

# -----------------------------
# Encode target
# -----------------------------
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

print("Classes:", label_encoder.classes_)
print("Total features:", X.shape[1])

# -----------------------------
# Train/Test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training:", len(X_train))
print("Testing:", len(X_test))

# -----------------------------
# Optimized XGBoost
# -----------------------------
print("\nTraining optimized model...")

model = XGBClassifier(
    n_estimators=1000,
    max_depth=9,
    learning_rate=0.035,
    min_child_weight=1,
    subsample=0.95,
    colsample_bytree=0.95,
    gamma=0,
    reg_alpha=0.01,
    reg_lambda=1,
    objective="multi:softmax",
    num_class=3,
    eval_metric="mlogloss",
    tree_method="hist",
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Prediction
# -----------------------------
print("\nPredicting...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n======================================")
print("OPTIMIZED ACCURACY:", round(accuracy * 100, 2), "%")
print("======================================")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

# -----------------------------
# Save model
# -----------------------------
with open("thermoguard_best.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoder_best.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

with open("feature_columns_best.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("\nModel saved:")
print("thermoguard_best.pkl")