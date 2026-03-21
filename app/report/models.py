from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Text

from app.core.database import Base
from app.report.enums import ReportStatus


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    saved_filename: Mapped[str] = mapped_column(String(255))
    status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus),
        default=ReportStatus.PENDING,
        server_default=ReportStatus.PENDING.value
    )
    result_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)