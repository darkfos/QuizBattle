from api.backend.exceptions.user_excception import *
from api.db.services.UserDbService import UserDatabaseService
from api.db.models.UserTable import User
from api.backend.schemas.UserPDSchema import *
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union


class UserAPIService:

    @staticmethod
    async def create_new_user(
        session: AsyncSession,
        user_data: AddNewUserPDSchema
    ) -> bool:
        """
        Return result operation - create user
        """

        new_user: User = User(
            telegram_id=user_data.telegram_id,
            name_user=user_data.name_user,
            score=user_data.score,
            date_create=user_data.date_create,
            date_update=user_data.date_update
        )
        
        result = await UserDatabaseService.add_record(session=session, new_user=new_user)

        if not result:
            return await http_400_create_error_user()
        
        return result