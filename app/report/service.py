import asyncio
import uuid
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy.ext.asyncio import AsyncSession

from app.report.analyzer import analyze_file
from app.report.excel_writer import create_report_xlsx
from app.core.config import settings
from app.report.dao import ReportDAO
from app.report.enums import ReportStatus

semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_TASKS)
executor = ProcessPoolExecutor()


def process_file(input_path: str, output_path: str):
    word_stats = analyze_file(input_path)
    create_report_xlsx(word_stats, output_path)

async def process_report(report_id: int, session: AsyncSession):
    async with semaphore:
        dao = ReportDAO(session)
        report = await dao.find_one_or_none(id=report_id)

        if not report:
            return

        await dao.update({"id": report_id}, status=ReportStatus.PROCESSING)
        await session.commit()

        input_path = f"{settings.UPLOAD_DIR}/{report.saved_filename}"
        result_filename = f"{uuid.uuid4()}.xlsx"
        output_path = f"{settings.RESULT_DIR}/{result_filename}"

        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, process_file, input_path, output_path)

            await dao.update(
                {"id": report_id},
                status=ReportStatus.COMPLETED,
                result_filename=result_filename,
            )
            await session.commit()

        except Exception as e:
            await dao.update(
                {"id": report_id},
                status=ReportStatus.FAILED,
                error_message=str(e),
            )
            await session.commit()