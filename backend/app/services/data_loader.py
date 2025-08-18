from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import re
import unicodedata

from ..config import get_settings

# Expected files and logical keys
EXPECTED_FILES: Dict[str, str] = {
    "historical": "DATA_Prêt_Années_Combiner.xlsx",
    "reporting": "Reporting_Visualisation.xlsx",
    "predictions": "Predictions_2mois_R.xlsx",
}

# In-memory cache for loaded DataFrames
_loaded_frames: Dict[str, pd.DataFrame] = {}


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def _normalize_name(name: str) -> str:
    name = _strip_accents(name).lower()
    # keep letters, digits and collapse separators
    name = re.sub(r"[^a-z0-9]+", "", name)
    return name


def _tokenize(name: str) -> List[str]:
    simple = _strip_accents(name).lower()
    return [tok for tok in re.findall(r"[a-z0-9]+", simple) if len(tok) >= 3]


def _probable_match(expected_filename: str, candidate_filename: str) -> bool:
    exp_norm = _normalize_name(expected_filename)
    cand_norm = _normalize_name(candidate_filename)
    if exp_norm == cand_norm:
        return True
    # Token containment heuristic: all expected tokens appear in candidate
    exp_tokens = _tokenize(expected_filename)
    return all(token in cand_norm for token in exp_tokens)


def _resolve_file(filename: str) -> Optional[Path]:
    settings = get_settings()
    candidate = settings.data_dir / filename
    if candidate.exists():
        return candidate

    # Try case-insensitive and normalized match among files in data dir
    for path in settings.data_dir.glob("*.xls*"):
        if path.name.lower() == filename.lower():
            return path
        if _probable_match(filename, path.name):
            return path
    return None


def resolve_expected_path(key: str) -> Optional[Path]:
    filename = EXPECTED_FILES.get(key)
    if not filename:
        return None
    return _resolve_file(filename)


def clear_cache() -> None:
    _loaded_frames.clear()


def load_all_datasets() -> Dict[str, pd.DataFrame]:
    global _loaded_frames
    for key, filename in EXPECTED_FILES.items():
        if key in _loaded_frames:
            continue
        path = _resolve_file(filename)
        if path is None:
            continue
        if key == "reporting":
            # reporting file has multiple sheets we care about
            try:
                xls = pd.ExcelFile(path)
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
                    _loaded_frames[f"reporting::{sheet_name}"] = df
            except Exception:
                # Fallback to reading default sheet
                df = pd.read_excel(path, engine="openpyxl")
                _loaded_frames["reporting::default"] = df
        else:
            df = pd.read_excel(path, engine="openpyxl")
            _loaded_frames[key] = df
    return _loaded_frames


def _find_client_columns(df: pd.DataFrame) -> List[str]:
    candidates = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(token in col_lower for token in ["client", "customer", "id", "code"]):
            candidates.append(str(col))
    return candidates


def get_clients() -> List[dict]:
    frames = load_all_datasets()

    # Prefer explicit client summary if present in reporting sheets
    for key, df in frames.items():
        if key.startswith("reporting::") and any(k in str(key).lower() for k in ["sammury", "summary", "client"]):
            cols = _find_client_columns(df)
            if cols:
                unique_clients = (
                    df[cols].dropna(how="all").drop_duplicates().to_dict(orient="records")
                )
                # Normalize keys
                normalized: List[dict] = []
                for row in unique_clients:
                    normalized.append(
                        {
                            "client_id": str(row.get("client_id") or row.get("Client_ID") or row.get("ID") or row.get(cols[0], "")).strip()
                            if any(k in (row.keys()) for k in ["client_id", "Client_ID", "ID"]) else None,
                            "client_name": str(row.get("client_name") or row.get("Client") or row.get("Nom_Client") or row.get("Name") or "").strip()
                            if any(k in (row.keys()) for k in ["client_name", "Client", "Nom_Client", "Name"]) else None,
                        }
                    )
                return normalized

    # Fallback: extract from historical
    hist = frames.get("historical")
    if hist is not None:
        cols = _find_client_columns(hist)
        if cols:
            unique_clients = (
                hist[cols].dropna(how="all").drop_duplicates().to_dict(orient="records")
            )
            normalized: List[dict] = []
            for row in unique_clients:
                normalized.append(
                    {
                        "client_id": str(row.get("client_id") or row.get("Client_ID") or row.get("ID") or row.get(cols[0], "")).strip()
                        if any(k in (row.keys()) for k in ["client_id", "Client_ID", "ID"]) else None,
                        "client_name": str(row.get("client_name") or row.get("Client") or row.get("Nom_Client") or row.get("Name") or "").strip()
                        if any(k in (row.keys()) for k in ["client_name", "Client", "Nom_Client", "Name"]) else None,
                    }
                )
            return normalized

    return []


def get_predictions() -> List[dict]:
    frames = load_all_datasets()

    # First choice: dedicated predictions file
    pred = frames.get("predictions")
    if pred is not None and not pred.empty:
        return pred.fillna("").to_dict(orient="records")

    # Second choice: reporting sheet likely named with prediction
    for key, df in frames.items():
        if key.startswith("reporting::") and any(token in key.lower() for token in ["prediction", "prédiction", "pred"]):
            return df.fillna("").to_dict(orient="records")

    return []


def get_client_history(client_name: str) -> List[dict]:
    frames = load_all_datasets()
    hist = frames.get("historical")
    if hist is None or hist.empty:
        return []
    # normalize
    df = hist.copy()
    if "Client" in df.columns:
        mask = df["Client"].astype(str).str.strip().str.lower() == client_name.strip().lower()
        df = df.loc[mask]
    else:
        return []

    if df.empty:
        return []

    # Ensure date is string ISO
    if "Date_Mois" in df.columns:
        try:
            df["Date_Mois"] = pd.to_datetime(df["Date_Mois"]).dt.strftime("%Y-%m-%d")
        except Exception:
            df["Date_Mois"] = df["Date_Mois"].astype(str)

    return df.fillna("").to_dict(orient="records")


def get_client_predictions(client_name: str) -> List[dict]:
    frames = load_all_datasets()
    pred = frames.get("predictions")
    if pred is None or pred.empty:
        return []
    df = pred.copy()
    col = None
    for candidate in ["Client", "client", "Nom_Client", "Name"]:
        if candidate in df.columns:
            col = candidate
            break
    if col is None:
        return []

    mask = df[col].astype(str).str.strip().str.lower() == client_name.strip().lower()
    df = df.loc[mask]
    if df.empty:
        return []
    return df.fillna("").to_dict(orient="records")