import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


print("=" * 60)
print("THERMOGUARD AI - LEAKAGE-FREE MODEL")
print("=" * 60)


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv("data_cleaned.csv", low_memory=False)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# 2. TARGET
# ============================================================

target = "risk_level"

print("\nTarget:", target)

print("\nRisk distribution:")
print(df[target].value_counts())


# ============================================================
# 3. REMOVE TARGET + DATA LEAKAGE FEATURES
# ============================================================

print("\nPreparing features...")

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
    if col in df.columns
]

X = df.drop(columns=drop_columns)
y = df[target]

print("\nRemoved columns:")
print(drop_columns)


# ============================================================
# 4. CATEGORICAL FEATURES
# ============================================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

print("\nCategorical columns:")
print(categorical_columns)


# One-hot encoding
X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

print("\nNumber of features:", X.shape[1])


# ============================================================
# 5. HANDLE MISSING / INFINITE VALUES
# ============================================================

print("\nChecking missing values...")

X = X.replace([np.inf, -np.inf], np.nan)

missing = X.isnull().sum().sum()

print("Missing values:", missing)

if missing > 0:
    X = X.fillna(X.median(numeric_only=True))
    X = X.fillna(0)


# ============================================================
# 6. ENCODE TARGET
# ============================================================

print("\nEncoding target...")

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

print("\nTarget classes:")

for i, label in enumerate(label_encoder.classes_):
    print(i, "=", label)


# ============================================================
# 7. TRAIN TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 8. RANDOM FOREST
# ============================================================

print("\n" + "=" * 60)
print("TRAINING RANDOM FOREST")
print("=" * 60)

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

print("\nTraining started...")
print("Please wait...")

model.fit(X_train, y_train)

print("\nTraining completed!")


# ============================================================
# 9. PREDICTION
# ============================================================

print("\nMaking predictions...")

y_pred = model.predict(X_test)


# ============================================================
# 10. ACCURACY
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print("\nAccuracy:", accuracy)
print(f"Accuracy Percentage: {accuracy * 100:.2f}%")


# ============================================================
# 11. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)


# ============================================================
# 12. CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")

cm = confusion_matrix(y_test, y_pred)

print(cm)


# ============================================================
# 13. FEATURE IMPORTANCE
# ============================================================

print("\nTop 15 Important Features:")

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print(
    importance.head(15).to_string(index=False)
)


# ============================================================
# 14. SAVE MODEL
# ============================================================

print("\n" + "=" * 60)
print("SAVING LEAKAGE-FREE MODEL")
print("=" * 60)

joblib.dump(
    model,
    "thermoguard_model_no_frp.pkl"
)

joblib.dump(
    label_encoder,
    "label_encoder_no_frp.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "feature_columns_no_frp.pkl"
)

print("\nFiles saved successfully:")

print("1. thermoguard_model_no_frp.pkl")
print("2. label_encoder_no_frp.pkl")
print("3. feature_columns_no_frp.pkl")


# ============================================================
# 15. FINAL
# ============================================================

print("\n" + "=" * 60)
print("THERMOGUARD AI - MODEL TRAINING COMPLETED")
print("=" * 60)

print("\nFRP was removed to prevent target leakage.")
print("The model is now ready for further evaluation.")
