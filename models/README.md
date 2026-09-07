# Models

All trained model artifacts, in one place. `backend/app/ml.py` is the
source of truth for which ones the running app actually loads.

## Active (loaded by `backend/app/ml.py`)

- `thermoguard_risk_v2.pkl`, `label_encoder_risk_v2.pkl`, `feature_columns_risk_v2.pkl` — the risk model, retrained on real burned-area outcome labels via `../data-pipeline/`. See its `README.md` and `output/models/metrics.json` for the honest evaluation.
- `thermoguard_fire_source_model.pkl`, `fire_source_label_encoder.pkl`, `fire_source_features.pkl` — fire-source classifier. Still the original, trained on FIRMS's own `type` field. `../data-pipeline/sources/landcover.py` provides a real replacement; not yet retrained (needs a more diverse data pull — see `../README.md`'s "Important limitations").

## Retired (not loaded by anything)

Kept for reference/rollback, not used by the app:

- `thermoguard_best.pkl` + its encoder/feature-columns — the original (FRP-threshold-labeled) risk model `thermoguard_risk_v2.pkl` replaced.
- `thermoguard_model.pkl`, `thermoguard_lightgbm.pkl`, `thermoguard_xgboost.pkl`, `thermoguard_xgboost_strong.pkl`, `thermoguard_frp_model.pkl` + their encoders/feature-columns — alternate model variants from `../legacy/`'s training scripts, never the one actually served.
- `feature_columns.pkl`, `label_encoder.pkl` — outputs of `../legacy/train_model.py`.
