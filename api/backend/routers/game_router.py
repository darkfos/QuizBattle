from fastapi import APIRouter, status, HTTPException
from api.backend.schemas.GamePDSchema import GameTranslate
from other.language.language_game import generator_word


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