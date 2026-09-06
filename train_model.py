import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("=" * 60)
print("THERMOGUARD AI - MODEL TRAINING")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv("data_cleaned.csv", low_memory=False)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# 2. CHECK TARGET
# ============================================================

target = "risk_level"

print("\nTarget column:", target)

print("\nRisk Level Distribution:")
print(df[target].value_counts())

print("\nRisk Level Percentage:")
print(df[target].value_counts(normalize=True) * 100)


# ============================================================
# 3. REMOVE UNNECESSARY COLUMNS
# ============================================================

print("\nPreparing features...")

drop_columns = [
    "risk_level",
    "acq_date",
    "datetime",
    "satellite",
    "instrument"
]

# Remove only columns that actually exist
drop_columns = [
    col for col in drop_columns
    if col in df.columns
]

X = df.drop(columns=drop_columns)
y = df[target]

print("Removed columns:", drop_columns)


# ============================================================
# 4. HANDLE CATEGORICAL FEATURES
# ============================================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

print("\nCategorical columns:")
print(categorical_columns)

# Convert categorical columns into numerical columns
X = pd.get_dummies(
    X,
    columns=categorical_columns,
    drop_first=True
)

print("\nFeatures after encoding:", X.shape[1])


# ============================================================
# 5. HANDLE MISSING / INFINITE VALUES
# ============================================================

print("\nChecking missing values...")

X = X.replace([np.inf, -np.inf], np.nan)

missing_values = X.isnull().sum().sum()

print("Total missing values:", missing_values)

if missing_values > 0:
    print("Filling missing values...")
    X = X.fillna(X.median(numeric_only=True))

    # If any remaining missing values exist
    X = X.fillna(0)


# ============================================================
# 6. ENCODE TARGET
# ============================================================

print("\nEncoding target labels...")

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

print("Target classes:")
for number, label in enumerate(label_encoder.classes_):
    print(number, "=", label)


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ============================================================
# 8. CREATE RANDOM FOREST MODEL
# ============================================================

print("\n" + "=" * 60)
print("TRAINING RANDOM FOREST")
print("=" * 60)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

print("\nTraining started...")
print("Please wait...")

model.fit(X_train, y_train)

print("\nTraining completed successfully!")


# ============================================================
# 9. MAKE PREDICTIONS
# ============================================================

print("\nMaking predictions...")

y_pred = model.predict(X_test)


# ============================================================
# 10. MODEL ACCURACY
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print("\nAccuracy:")
print(accuracy)

print("\nAccuracy Percentage:")
print(f"{accuracy * 100:.2f}%")


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

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print(feature_importance.head(15).to_string(index=False))


# ============================================================
# 14. SAVE MODEL
# ============================================================

print("\n" + "=" * 60)
print("SAVING MODEL")
print("=" * 60)

joblib.dump(
    model,
    "thermoguard_model.pkl"
)

joblib.dump(
    label_encoder,
    "label_encoder.pkl"
)

joblib.dump(
    X.columns.tolist(),
    "feature_columns.pkl"
)

print("\nModel saved:")
print("1. thermoguard_model.pkl")
print("2. label_encoder.pkl")
print("3. feature_columns.pkl")


# ============================================================
# 15. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("THERMOGUARD AI MODEL TRAINING COMPLETED!")
print("=" * 60)

print("\nThe trained model is ready for prediction.")