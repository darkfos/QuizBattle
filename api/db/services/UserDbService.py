from abs_fabric import CRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, delete, update
from sqlalchemy.orm import joinedload
from api.db.models.UserTable import User
from typing import Union, List


class UserDatabaseService(CRUDRepository):

    @staticmethod
    async def add_record(
        session: AsyncSession,
        new_user: User
    ) -> bool:
        try:
            await session.execute(new_user)
            await session.commit()
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_one(
        session: AsyncSession,
        user_id: int
    ) -> Union[bool, User]:
        try:
            stmt = select(User).where(User.id == user_id)
            sel = await session.execute(stmt)
            result: Result = sel.one_or_none()

            if result:
                return result[0]
            else:
                return False
        except Exception as ex:
            return False
        finally:
            await session.close()
    
    @staticmethod
    async def get_all_records(
        session: AsyncSession
    ) -> Union[bool, List]:
        try:
            stmt = select(User)
            sel = await session.execute(stmt)
            result: Result = sel.all()

            if result:
                return result
            else:
                return []
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def update_record(
        session: AsyncSession,
        user_id: int,
        new_data: ...
    ) -> bool:
        try:

            stmt = update(User).where(User.id == user_id).values(**new_data)
            await session.execute(stmt)
            await session.commit()

        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def del_record(
        session: AsyncSession,
        user_id: int
    ) -> bool:
        try:
            stmt = delete(User).where(User.id == user_id)
            await session.execute(stmt)
            await session.commit()
            return True
        except Exception as ex:
            return False
        finally:
            await session.close()
    
    @staticmethod
    async def get_all_history_user(
        session: AsyncSession,
        user_id: int
    ) -> Union[List]:
        try:
            stmt = select(User).options(joinedload(User.history)).where(User.id == user_id)
            sel = await session.execute(stmt)
            result: Result = sel.all()

            if result:
                return result
            else:
                return []
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def get_all_reviews_user(
        session: AsyncSession,
        user_id: int
    ) -> Union[List]:
        try:
            stmt = select(User).options(joinedload(User.reviews)).where(User.id == user_id)
            sel = await session.execute(stmt)
            result: Result = sel.all()

            if result:
                return result
            else:
                return []
        except Exception as ex:
            return False
        finally:
            await session.close()