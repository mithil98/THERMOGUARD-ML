import joblib
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("THERMOGUARD AI - FEATURE IMPORTANCE")
print("=" * 60)

# Load model
model = joblib.load("thermoguard_model_no_frp.pkl")

# Load feature names
feature_columns = joblib.load("feature_columns_no_frp.pkl")

# Get feature importance
importance = model.feature_importances_

# Create dataframe
importance_df = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": importance
})

# Sort by importance
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 15 Important Features:")
print(importance_df.head(15).to_string(index=False))

# Select top 15
top_features = importance_df.head(15).sort_values(
    by="Importance"
)

# Create graph
plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("ThermoGuard AI - Top 15 Feature Importance")

plt.tight_layout()

# Save graph
plt.savefig(
    "feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nSaved: feature_importance.png")

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE COMPLETED")
print("=" * 60)