# Backend (FastAPI)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## Data
Place your Excel files in `backend/data/` with these names (or upload via API):
- DATA_Prêt_Années_Combiner.xlsx
- Reporting_Visualisation.xlsx (sheets: `Prédiction_R`, `Sammury_Client`)
- Predictions_2mois_R.xlsx

## Endpoints
- GET `/health`
- GET `/data/status`
- POST `/data/upload` (form field `file`)
- POST `/data/load`
- GET `/clients`
- GET `/predictions`