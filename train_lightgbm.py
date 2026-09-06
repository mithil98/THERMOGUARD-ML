import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from lightgbm import LGBMClassifier

print("Loading dataset...")

df = pd.read_csv("data_cleaned.csv", low_memory=False)

target = "risk_level"

drop_columns = [
    "risk_level",
    "frp",
    "acq_date",
    "datetime",
    "satellite",
    "instrument"
]

X = df.drop(columns=drop_columns, errors="ignore")
y = df[target]

# Encode categorical columns
categorical_columns = [
    "confidence",
    "version",
    "daynight",
    "season"
]

for col in categorical_columns:
    if col in X.columns:
        X[col] = pd.Categorical(X[col]).codes

X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)

# Encode target
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

print("Classes:", label_encoder.classes_)
print("Features:", X.shape[1])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nTraining LightGBM model...")

model = LGBMClassifier(
    n_estimators=800,
    learning_rate=0.05,
    max_depth=10,
    num_leaves=63,
    min_child_samples=20,
    subsample=0.90,
    colsample_bytree=0.90,
    reg_alpha=0.05,
    reg_lambda=1.0,
    objective="multiclass",
    num_class=3,
    random_state=42,
    n_jobs=-1,
    verbosity=-1
)

model.fit(X_train, y_train)

print("\nPredicting...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n======================================")
print("LIGHTGBM ACCURACY:", round(accuracy * 100, 2), "%")
print("======================================")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

# Save model separately
with open("thermoguard_lightgbm.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoder_lightgbm.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

with open("feature_columns_lightgbm.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("\nModel saved successfully!")
print("thermoguard_lightgbm.pkl")