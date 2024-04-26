from pydantic import BaseModel, Field
from typing import List, Union, Annotated


class HistoryBasePDSchema(BaseModel):

    score: Annotated[int, Field()]
    right_word: Annotated[int, Field()]
    lose_word: Annotated[int, Field()]
    procent_game: Annotated[float, Field()]


class AddNewHistoryPDSchema(HistoryBasePDSchema):
    pass


class GetHistoryPDSchema(HistoryBasePDSchema):
    pass