from pydantic import Field, BaseModel


class GameTranslate(BaseModel):

    secret_word: str = Field()
    translate_in_russo: str = Field()