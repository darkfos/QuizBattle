from fastapi import APIRouter, status, HTTPException, Depends
from api.backend.schemas.GamePDSchema import GameTranslate, StatsUser
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.db_engine import db_worker
from other.language.language_game import generator_word
from api.backend.services.UserService import UserAPIService
from typing import List, Annotated, Union


game_router: APIRouter = APIRouter(
    prefix="/game",
    tags=["Game"]
)


@game_router.get("/random_word/{language_code}", status_code=status.HTTP_201_CREATED, response_model=GameTranslate)
async def random_word(
    language_code: str
) -> GameTranslate:
    try:
        gen_words: dict = generator_word.get_random_word(attr_lng=language_code)
        return GameTranslate(
            secret_word=gen_words.get("word"),
            translate_in_russo=gen_words.get("translate")
        )
    
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось сгенерировать слова, возможно вы передали не ту кодировку языка"
        )
    

@game_router.get("/game_stats",
                 status_code=status.HTTP_200_OK,
                 response_model=Union[List, List[StatsUser]])
async def get_stats_about_all_users(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: str,
) -> Union[List, List[StatsUser]]:
    
    res = await UserAPIService().get_all_users_order_by_score(session=session, token=token)
    return res


@game_router.get("/top_rank",
                 status_code=status.HTTP_200_OK)
async def get_user_rank(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: str
) -> dict:
    
    res = await UserAPIService().get_all_users_order_by_score(session=session, token=token, flag=True)

    return res