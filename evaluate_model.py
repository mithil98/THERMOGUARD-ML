import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

print("=" * 60)
print("THERMOGUARD AI - MODEL EVALUATION")
print("=" * 60)

print("\nLoading dataset...")
df = pd.read_csv("data_cleaned.csv", low_memory=False)

print("Dataset loaded!")
print("Dataset shape:", df.shape)

# Load saved model information
model = joblib.load("thermoguard_model_no_frp.pkl")
label_encoder = joblib.load("label_encoder_no_frp.pkl")
feature_columns = joblib.load("feature_columns_no_frp.pkl")

# Remove columns that should not be used
remove_columns = [
    "risk_level",
    "frp",
    "acq_date",
    "datetime",
    "satellite",
    "instrument"
]

X = df.drop(columns=remove_columns, errors="ignore")
y = label_encoder.transform(df["risk_level"])

# Convert categorical columns using one-hot encoding
categorical_columns = X.select_dtypes(include=["object"]).columns.tolist()

print("\nCategorical columns:")
print(categorical_columns)

X = pd.get_dummies(X, columns=categorical_columns, drop_first=False)

# Make sure X has exactly the same columns as the trained model
X = X.reindex(columns=feature_columns, fill_value=0)

print("\nNumber of features:", X.shape[1])

# Convert everything to numeric
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

# Same test split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nMaking predictions...")
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("TEST SET RESULTS")
print("=" * 60)

print(f"\nAccuracy: {accuracy:.4f}")
print(f"Accuracy Percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

# Save confusion matrix image
plt.figure(figsize=(8, 6))
plt.imshow(cm)
plt.title("ThermoGuard AI - Confusion Matrix")
plt.xlabel("Predicted Risk")
plt.ylabel("Actual Risk")

plt.xticks(
    range(len(label_encoder.classes_)),
    label_encoder.classes_
)

plt.yticks(
    range(len(label_encoder.classes_)),
    label_encoder.classes_
)

for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=300)
plt.close()

print("\nSaved: confusion_matrix.png")

print("\n" + "=" * 60)
print("EVALUATION COMPLETED SUCCESSFULLY")
print("=" * 60)