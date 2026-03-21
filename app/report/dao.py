from app.core.base_dao import BaseDAO
from app.report.models import Report


class ReportDAO(BaseDAO):
    model = Report