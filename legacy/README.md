# Legacy

Superseded model-training code, kept for historical reference only — none
of it is used by the running app.

- **`train_best.py`, `train_with_frp.py`, `train_model.py`, `train_model_no_frp.py`, `train_lightgbm.py`, `train_xgboost.py`** — six divergent training scripts, all reading an undocumented `data_cleaned.csv` (not in this repo) with an FRP-threshold-derived `risk_level` label. Replaced by `data-pipeline/train.py`, which trains on real, sourced outcome labels instead. See `data-pipeline/README.md`.
- **`predict.py`, `predict_no_frp.py`** — CLI scripts for manually checking a trained model's prediction against a dataset row. Depend on the same missing `data_cleaned.csv`.
- **`evaluate_model.py`, `feature_importance.py`** — offline evaluation utilities for the `_no_frp` model variant; produced `confusion_matrix.png` and `feature_importance.png`, kept alongside them here.
- **`frp_model_integration_notes.txt`** — the original integration spec for the FRP-inclusive model variant (`thermoguard_frp_model.pkl` in `../models/`).
- **`requirements.txt`** — dependencies for the scripts in this folder (pandas, scikit-learn, xgboost, lightgbm, matplotlib, joblib). The active app has its own, narrower requirements files: `../backend/requirements.txt` and `../data-pipeline/requirements.txt`.

None of these scripts will run as-is — they depend on a dataset that was
never checked into this repo. They're kept for provenance, not as a
working pipeline.
