from api.backend.exceptions.user_excception import *
from api.db.services.UserDbService import UserDatabaseService
from api.db.models.UserTable import User
from api.backend.schemas.UserPDSchema import *
from api.backend.schemas.TokenPDSchema import GetAccessToken
from sqlalchemy.ext.asyncio import AsyncSession
from api.backend.auth.security import SecurityAPI
from api.db.models.UserTable import User
from sqlalchemy import select
from typing import List, Union


security_app: SecurityAPI = SecurityAPI()


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

    @staticmethod
    async def get_user_info(
        session: AsyncSession,
        token: str
    ) -> UserBasePDSchema:
        """
        Get basic information about user
        """

        #Get user id
        res: dict = await security_app.decode_jwt(token=token)
        user_id: int = res.get("user_id")

        user_information: User = await UserDatabaseService.get_one(
            session=session,
            user_id=user_id
        )

        if user_information:
            return UserBasePDSchema(
                name_user=user_information.name_user,
                score=user_information.score,
                game_count=user_information.game_count,
                date_create=user_information.date_create,
                date_update=user_information.date_update
            )
        
        await http_400_user_not_found()
    
    @staticmethod
    async def get_full_information_about_user(
        session: AsyncSession,
        token: str
    ) -> UserBasePDSchema:
        """
        Get full information about user
        """

        #Get user id
        user_id: int = (await security_app.decode_jwt(token=token)).get("user_id")

        user_full_information: User = await UserDatabaseService.get_full_information(
            session=session,
            user_id=user_id
        )

        response: UserFullInformationPDSchema = UserFullInformationPDSchema(
            name_user=user_full_information.name_user,
            score=user_full_information.score,
            game_count=user_full_information.game_count,
            date_create=user_full_information.date_create,
            date_update=user_full_information.date_update,
            histories=[
                GetHistoryPDSchema(
                    score=history.score,
                    right_word=history.right_word,
                    lose_word=history.lose_word,
                    procent_game=history.procent_game
                )
                    for history in user_full_information.history
            ] if len(user_full_information.history) > 0 else [],
            reviews=[
                GetReviewPDSchema(
                    message=review.message
                )
                    for review in user_full_information.reviews
                ] if len(user_full_information.reviews) > 0 else []
        )

        return response

    @staticmethod
    async def update_user(
        session: AsyncSession,
        user_data: UpdateUserInfoPDSchema,
        flag: bool = False
    ) -> UserIsUpdated:
        """
        Update information about user
        """

        #Get user id
        data_from_token: dict = await security_app.decode_jwt(token=user_data.token)

        await security_app.user_is_created(
            session=session,
            telegram_id=data_from_token.get("tg_id")
            )
        
        sel = select(User).where(User.id == data_from_token.get("user_id"))
        res: User = (( await session.execute(sel) ).one_or_none())[0]

        if flag == "count":
            is_updated: bool = await UserDatabaseService.update_record(
                session=session,
                user_id=data_from_token.get("user_id"),
                new_data={"game_count": user_data.game_count + (res.game_count if res.game_count else 0)}
            )

        elif flag == True:
            is_updated: bool = await UserDatabaseService.update_record(
                session=session,
                user_id=data_from_token.get("user_id"),
                new_data={"score": user_data.score + res.score}
            )
        else:
            is_updated: bool = await UserDatabaseService.update_record(
                session=session,
                user_id=data_from_token.get("user_id"),
                new_data={"name_user": user_data.name_user, "date_update": user_data.date_update}
            )

        return UserIsUpdated(is_updated=is_updated)

    @staticmethod
    async def delete_user(
        session: AsyncSession,
        token: GetAccessToken
    ) -> UserIsDeletedPDSchema:
        """
        Delete user
        """

        #Get user id
        data_from_token: dict = await security_app.decode_jwt(token=token.token)
        
        await security_app.user_is_created(telegram_id=data_from_token.get("tg_id"), session=session)

        is_deleted: bool = await UserDatabaseService.del_record(session=session, user_id=data_from_token.get("user_id"))

        return UserIsDeletedPDSchema(is_deleted=is_deleted)