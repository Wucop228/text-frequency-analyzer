import uuid

import aiofiles
from fastapi import UploadFile

from app.core.config import settings


async def save_upload_file(file: UploadFile) -> tuple[str, str]:
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "txt"
    saved_filename = f"{uuid.uuid4()}.{ext}"
    filepath = f"{settings.UPLOAD_DIR}/{saved_filename}"

    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(settings.FILE_READ_CHUNK_SIZE):
            await f.write(chunk)

    return file.filename, saved_filename