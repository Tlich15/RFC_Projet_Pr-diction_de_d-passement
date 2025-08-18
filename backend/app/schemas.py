from typing import List, Optional
from pydantic import BaseModel


class FileStatus(BaseModel):
    name: str
    exists: bool
    path: Optional[str] = None


class DatasetSummary(BaseModel):
    name: str
    num_rows: int
    num_columns: int
    columns: List[str]


class DataLoadResponse(BaseModel):
    files: List[FileStatus]
    summaries: List[DatasetSummary]


class ClientRecord(BaseModel):
    client_id: Optional[str] = None
    client_name: Optional[str] = None