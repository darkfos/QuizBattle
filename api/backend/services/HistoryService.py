from sqlalchemy.ext.asyncio import AsyncSession
from api.backend.schemas.HistoryPDSchema import *
from api.db.services.HistoryDbService import HistoryDatabaseService
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