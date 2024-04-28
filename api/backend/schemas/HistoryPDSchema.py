from pydantic import BaseModel, Field
from typing import List, Union, Annotated


class HistoryBasePDSchema(BaseModel):

    score: Annotated[int, Field()]
    right_word: Annotated[int, Field()]
    lose_word: Annotated[int, Field()]
    procent_game: Annotated[float, Field()]


class AddNewHistoryPDSchema(HistoryBasePDSchema):
    
    #Add attr
    token: Annotated[str, Field()]


class GetHistoryPDSchema(HistoryBasePDSchema):
    pass


class HistoryIsCreatedPDSchema(BaseModel):

    is_created: bool