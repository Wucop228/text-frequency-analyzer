from sqlalchemy import update as sa_update
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, **data):
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, filter_by: dict, **data):
        stmt = (
            sa_update(self.model)
            .filter_by(**filter_by)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one_or_none()