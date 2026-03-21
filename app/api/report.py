import asyncio

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.report.schemas import ReportResponse
from app.core.database import get_db
from app.report.dao import ReportDAO
from app.core.config import settings
from app.report.service import process_report
from app.report.utils import save_upload_file

router = APIRouter(prefix="/public/report", tags=["reports"])

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, session: AsyncSession = Depends(get_db)):
    dao = ReportDAO(session)
    report = await dao.find_one_or_none(id=report_id)

    if not report:
        raise HTTPException(status_code=404, detail="report not found")

    return report

@router.post("/export", response_model=ReportResponse)
async def export_report(file: UploadFile, session: AsyncSession = Depends(get_db)):
    original_filename, saved_filename = await save_upload_file(file)

    dao = ReportDAO(session)
    report = await dao.add(
        original_filename=original_filename,
        saved_filename=saved_filename,
    )
    await session.commit()

    asyncio.create_task(process_report(report.id))

    return report

@router.get("/{report_id}/download")
async def download_report(report_id: int, session: AsyncSession = Depends(get_db)):
    dao = ReportDAO(session)
    report = await dao.find_one_or_none(id=report_id)

    if not report or not report.result_filename:
        raise HTTPException(status_code=404, detail="report not found or not ready")

    filepath = f"{settings.RESULT_DIR}/{report.result_filename}"
    return FileResponse(
        path=filepath,
        filename=f"report_{report.original_filename}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )