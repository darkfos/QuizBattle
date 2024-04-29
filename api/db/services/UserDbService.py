from abs_fabric import CRUDRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select, delete, update, desc
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
            session.add(new_user)
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
            sel: Result = await session.execute(stmt)
            result = sel.one_or_none()

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
            sel: Result = await session.execute(stmt)
            result = sel.all()

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
        new_data: dict
    ) -> bool:
        try:

            stmt = update(User).where(User.id == user_id).values(**new_data)
            await session.execute(stmt)
            await session.commit()
            return True

        except Exception as ex:
            print(ex)
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
            print(ex)
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
            sel: Result = await session.execute(stmt)
            result = sel.all()

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
            sel: Result = await session.execute(stmt)
            result = sel.all()

            if result:
                return result
            else:
                return []
        except Exception as ex:
            return False
        finally:
            await session.close()

    @staticmethod
    async def find_user_by_tg_id(
        session: AsyncSession,
        tg_id: int
    ) -> Union[bool, int]:
        """
        Find user by tg_id
        """

        try:
            stmt = select(User).where(User.telegram_id == tg_id)
            sel: Result = await session.execute(stmt)
            result = sel.one_or_none()

            if result:
                return result[0].id
            raise ex
        except Exception as ex:
            return False
        finally:
            await session.close()
    
    @staticmethod
    async def get_full_information(
        session: AsyncSession,
        user_id: int
    ) -> User:
        
        try:
            stmt = select(User).options(
                joinedload(User.reviews),
                joinedload(User.history)
            ).where(User.id == user_id)

            res: Result = (await session.execute(stmt)).unique()

            if res:
                return res.one()[0]
            raise ex
        
        except Exception as ex:
            return False
        finally:
            await session.close()
    
    @staticmethod
    async def get_all_records_order_score(session: AsyncSession):
        try:
            stmt = select(User).order_by(desc(User.score))

            res: Result = await session.execute(stmt)

            if res:
                return res.all()[0]
            raise ex
        
        except Exception as ex:
            return False
        finally:
            await session.close()