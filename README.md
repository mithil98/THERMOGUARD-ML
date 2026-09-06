# ThermoGuard AI

AI-based wildfire risk prediction and fire source analysis, built on NASA satellite hotspot telemetry (brightness, FRP, scan/track geometry, day/night, confidence).

The project has two parts:

- **`backend/`** — a FastAPI service that loads the trained XGBoost models and exposes prediction, fire-source classification, and PDF-report endpoints.
- **`frontend/`** — a React + TypeScript + Tailwind CSS single-page app that drives those endpoints, with a live-slider risk simulator, a fire location map, and a downloadable PDF report.

Model training scripts and datasets used to produce the `.pkl` model files live at the repo root (`train_*.py`, `evaluate_model.py`, `feature_importance.py`).

## Prerequisites

| Tool | Version | Check |
|---|---|---|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |

## 1. Clone the repo

```bash
git clone https://github.com/mithil98/THERMOGUARD-ML.git
cd THERMOGUARD-ML
```

## 2. Backend setup (FastAPI)

From the repo root:

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r backend/requirements.txt
```

Run the API server (from the repo root, so it can find the `.pkl` model files):

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Verify it's up:

```bash
curl http://localhost:8000/api/health
# {"risk_model_ready":true,"fire_source_model_ready":true,"error":null}
```

Interactive API docs: http://localhost:8000/docs

## 3. Frontend setup (React + Vite)

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. The dev server proxies `/api/*` requests to the backend on port 8000 (see `frontend/vite.config.ts`), so both servers need to be running.

## 4. Using the app

1. Fill in the satellite hotspot parameters (location, brightness, FRP, acquisition time, etc.) — sensible defaults are pre-filled.
2. Drag the **Live Fire Risk Interaction** sliders to see the risk level and probabilities update in real time.
3. Click **Analyze Fire Risk** for the full report: risk level, fire source classification, intensity/thermal/temporal analysis, alert assessment, probability breakdown, and a location map.
4. Click **Download PDF Report** to save a formatted report of the current analysis.

## Production build

```bash
cd frontend
npm run build      # outputs to frontend/dist
npm run preview    # serve the production build locally
```

Serve `frontend/dist` with any static host, and run the backend with a production ASGI server, e.g.:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Update the frontend's API base URL / proxy configuration if the backend isn't reachable at the same origin in production.

## Project structure

```
THERMOGUARD-ML/
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app, route wiring
│   │   ├── ml.py           # model loading, feature engineering, prediction
│   │   ├── report.py        # PDF report generation
│   │   └── schemas.py        # request/response models
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # UI sections (form, results, charts, map, ...)
│   │   ├── components/fx/   # animated UI primitives
│   │   ├── lib/               # API client, helpers
│   │   └── App.tsx
│   └── package.json
├── train_*.py                # model training scripts
├── evaluate_model.py           # model evaluation
├── feature_importance.py        # feature importance analysis
└── *.pkl                          # trained models, encoders, feature lists
```

## Important limitations

- **Fire Detection** is a preliminary rule-based thermal screening (FRP ≥ 2.40 and brightness difference ≥ 15), not a separately trained binary Fire/No-Fire classifier.
- **Fire Source** categories (Vegetation Fire, Other Land Source, Offshore, Unknown) come from the dataset's hotspot source classes — the dataset does not provide direct Forest/Agriculture/Industrial labels, so "Other Land Source" must not be read as confirmed industrial activity.
- The reported model accuracy is strongly influenced by FRP in the training dataset and should not be interpreted as independent real-world wildfire prediction accuracy.
