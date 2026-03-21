from datetime import datetime

from pydantic import BaseModel

from app.report.enums import ReportStatus


class ReportResponse(BaseModel):
    id: int
    original_filename: str
    status: ReportStatus
    result_filename: str | None = None
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}