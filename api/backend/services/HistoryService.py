from sqlalchemy.ext.asyncio import AsyncSession
from api.backend.schemas.HistoryPDSchema import *
from api.db.services.HistoryDbService import HistoryDatabaseService
from api.backend.exceptions.history_exception import *
from api.db.models.HistoryTable import History
from api.backend.auth.security import SecurityAPI



app_security: SecurityAPI = SecurityAPI()


class HistoryAPIService:

    @staticmethod
    async def add_a_new_history(
        session: AsyncSession,
        new_history: AddNewHistoryPDSchema
    ) -> HistoryIsCreatedPDSchema:
        """
        Create new history
        """

        #Get user data
        data_from_token: dict = await app_security.decode_jwt(token=new_history.token)

        
        #User is created?
        await app_security.user_is_created(session=session, telegram_id=data_from_token.get("tg_id"))
        
        is_created: bool = await HistoryDatabaseService.add_record(
            session=session,
            new_history=History(
            score=new_history.score,
            right_word=new_history.right_word,
            lose_word=new_history.lose_word,
            procent_game=new_history.procent_game,
            user_id=data_from_token.get("user_id")
            )
        )

        return HistoryIsCreatedPDSchema(
            is_created=is_created
        )
    
    @staticmethod
    async def get_history_by_id(session: AsyncSession, id: int) -> GetHistoryPDSchema:
        """
        Return GetHistoryPDSchema
        """

        result = await HistoryDatabaseService.get_one(session=session, history_id=id)

        if result:
            return GetHistoryPDSchema(
                score=result.score,
                right_word=result.right_word,
                lose_word=result.lose_word,
                procent_game=result.procent_game
            )

        await http_404_error_get_history()
    
    @staticmethod
    async def get_all_history_for_user(session: AsyncSession, token: str) -> Union[List, List[GetHistoryPDSchema]]:
        """
        return List[GetHistoryPDSchema]
        """

        #Get user id
        user_id: int = ( await app_security.decode_jwt(token=token) ).get("user_id")

        result = await HistoryDatabaseService.get_all_histories_by_user_id(session=session, user_id=user_id)
        
        if result:
            
            results: List[GetHistoryPDSchema] = [
                
                GetHistoryPDSchema(
                    score=history[0].score,
                    right_word=history[0].right_word,
                    lose_word=history[0].lose_word,
                    procent_game=history[0].procent_game
                )
                    for history in result
            ]

            return results
        else:   
            return []
    
    @staticmethod
    async def delete_history(
        session: AsyncSession,
        history_id: int
    ) -> HistoryIsDeletedPDSchema:
        """
        Delete history
        """

        is_deleted: bool = await HistoryDatabaseService.del_record(session=session, history_id=history_id)

        return HistoryIsDeletedPDSchema(
            is_deleted=is_deleted
        )