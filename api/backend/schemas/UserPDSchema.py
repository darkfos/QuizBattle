from pydantic import Field, BaseModel
from typing import Annotated, Union, List
from datetime import datetime
from api.backend.schemas.HistoryPDSchema import GetHistoryPDSchema
from api.backend.schemas.ReviewPDSchema import GetReviewPDSchema


class UserBasePDSchema(BaseModel):
    
    name_user: Annotated[str, Field(max_length=500)]
    score: Annotated[int, Field()]
    date_create: datetime
    date_update: datetime


class UserAndHistoryPDSchema(UserBasePDSchema):

    #Add attr
    histories: List[GetHistoryPDSchema]


class UserAndReviewsPDSchema(UserBasePDSchema):

    #Add attr
    reviews: List[GetReviewPDSchema]


class AddNewUserPDSchema(UserBasePDSchema):
    pass


class UpdateUserInfoPDSchema(BaseModel):

    telegram_id: Annotated[int, Field]
    name_user: Annotated[str, Field(max_length=500)]
    date_update: datetime


class UpdateUserScore(BaseModel):

    telegram_id: Annotated[int, Field()]
    score: Annotated[int, Field()]