from abs_fabric import CRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, delete, update
from sqlalchemy.orm import joinedload
from api.db.models.HistoryTable import History
from typing import Union, List


class HistoryDatabaseService(CRUDRepository):

    @staticmethod
    async def add_record(
        session: AsyncSession,
        new_history: History
    ) -> bool:
        try:
            await session.add(new_history)
            await session.commit()
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_all_records(
        session: AsyncSession,
    ) -> Union[bool, List]:
        try:
            stmt = select(History)
            sel: Result = await session.execute(stmt)
            result = sel.all()

            if result: return result
            else: return []
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_one(
        session: AsyncSession,
        history_id: int
    ) -> Union[bool, History]:
        try:
            stmt = select(History).where(History.id == history_id)
            sel: Result = await session.execute(stmt)
            result = sel.one_or_none()

            if result: return result[0]
            else:
                raise ex
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def update_record(
        session: AsyncSession,
        history_id: int,
        new_history: History
    ) -> None:
        pass

    @staticmethod
    async def del_record(
        session: AsyncSession,
        history_id: int
    ) -> bool:
        try:
            del_history = delete(History).where(History.id == history_id)
            await session.execute(del_history)
            await session.commit()
        except Exception as ex:
            return False
        finally:
            await session.close()