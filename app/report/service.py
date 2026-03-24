import asyncio
import uuid
from concurrent.futures import ProcessPoolExecutor
import time

from loguru import logger

from app.report.analyzer import analyze_file
from app.report.excel_writer import create_report_xlsx
from app.core.config import settings
from app.report.dao import ReportDAO
from app.report.enums import ReportStatus
from app.core.database import async_session_maker

semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_TASKS)
executor = ProcessPoolExecutor(max_workers=settings.MAX_CONCURRENT_TASKS)


def process_file(input_path: str, output_path: str):
    word_stats = analyze_file(input_path)
    create_report_xlsx(word_stats, output_path)

async def process_report(report_id: int):
    logger.info("report id={} added in queue", report_id)

    async with semaphore:
        async with async_session_maker() as session:
            dao = ReportDAO(session)
            report = await dao.find_one_or_none(id=report_id)

            if not report:
                logger.error("report id={} not found in DB", report_id)
                return

            await dao.update({"id": report_id}, status=ReportStatus.PROCESSING)
            await session.commit()

            input_path = f"{settings.UPLOAD_DIR}/{report.saved_filename}"
            result_filename = f"{uuid.uuid4()}.xlsx"
            output_path = f"{settings.RESULT_DIR}/{result_filename}"

            start_time = time.time()
            logger.info("report id={} processing", report_id)

            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(executor, process_file, input_path, output_path)

                end_time = time.time()
                await dao.update(
                    {"id": report_id},
                    status=ReportStatus.COMPLETED,
                    result_filename=result_filename,
                )
                await session.commit()
                logger.info("report id={} done in {:.1f}s", report_id, end_time - start_time)

            except Exception as e:
                end_time = time.time()
                await dao.update(
                    {"id": report_id},
                    status=ReportStatus.FAILED,
                    error_message=str(e),
                )
                await session.commit()
                logger.exception("report id={} failed after {:.1f}s", report_id, end_time - start_time)