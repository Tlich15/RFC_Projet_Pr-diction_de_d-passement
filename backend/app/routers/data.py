from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException

from ..config import get_settings
from ..schemas import DataLoadResponse, DatasetSummary, FileStatus
from ..services import data_loader

router = APIRouter()


@router.get("/status", response_model=List[FileStatus])
def get_data_status() -> List[FileStatus]:
    statuses: List[FileStatus] = []
    for key, expected_name in data_loader.EXPECTED_FILES.items():
        resolved = data_loader.resolve_expected_path(key)
        statuses.append(
            FileStatus(
                name=key,
                exists=resolved is not None,
                path=str(resolved) if resolved else None,
            )
        )
    return statuses


@router.post("/upload", response_model=FileStatus)
async def upload_excel(file: UploadFile = File(...)) -> FileStatus:
    settings = get_settings()
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")

    dest_path = settings.data_dir / file.filename
    content = await file.read()
    dest_path.write_bytes(content)

    # Invalidate cache if any
    data_loader.clear_cache()

    # Try to infer key if filename matches expected ones
    inferred_key = None
    for key, expected_name in data_loader.EXPECTED_FILES.items():
        if expected_name.lower() == file.filename.lower():
            inferred_key = key
            break

    return FileStatus(name=inferred_key or file.filename, exists=True, path=str(dest_path))


@router.post("/load", response_model=DataLoadResponse)
def load_all() -> DataLoadResponse:
    loaded = data_loader.load_all_datasets()

    summaries: List[DatasetSummary] = []
    for name, df in loaded.items():
        summaries.append(
            DatasetSummary(
                name=name,
                num_rows=int(df.shape[0]),
                num_columns=int(df.shape[1]),
                columns=[str(c) for c in df.columns.tolist()],
            )
        )

    files_status = get_data_status()
    return DataLoadResponse(files=files_status, summaries=summaries)