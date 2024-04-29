from pydantic import Field, BaseModel


class GameTranslate(BaseModel):

    secret_word: str = Field()
    translate_in_russo: str = Field()


class StatsUser(BaseModel):

    user_name: str = Field()
    score: int = Field()