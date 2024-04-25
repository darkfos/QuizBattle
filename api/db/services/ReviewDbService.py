from abs_fabric import CRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, delete, update
from sqlalchemy.orm import joinedload
from api.db.models.ReviewTable import Review
from typing import Union, List


class ReviewDatabaseService(CRUDRepository):

    @staticmethod
    async def get_one(
        session: AsyncSession,
        review_id: int
    ) -> Union[bool, Review]:
        try:
            stmt = select(Review).where(Review.id == review_id)
            sel: Result = await session.execute(stmt)
            result = sel.one_or_none()

            if result: return result[0]
            raise ex
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_all_records(
        session: AsyncSession
    ) -> Union[bool, List]:
        try:
            stmt = select(Review)
            sel: Result = await session.execute(stmt)
            result = sel.all()

            if result: return result
            else: return []
        except Exception as ex:
            return False
        finally:
            await session.close()
    
    @staticmethod
    async def add_record(
        session: AsyncSession,
        new_record: Review
    ) -> bool:
        try:
            await session.add(new_record)
            await session.commit()
        except Exception as ex:
            return False
        finally:
            await session.close()
    
    @staticmethod
    async def update_record(
        session: AsyncSession
    ) -> None:
        pass

    @staticmethod
    async def delete_record(
        session: AsyncSession
    ) -> bool:
        pass