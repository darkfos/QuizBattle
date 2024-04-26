from pydantic import Field, BaseModel
from typing import Annotated, Union, List
from datetime import datetime


class UserBasePDSchema(BaseModel):
    
    name_user: Annotated[str, Field(max_length=500)]
    score: Annotated[int, Field()]
    date_create: datetime
    date_update: datetime


class UserAndHistoryPDSchema(UserBasePDSchema):

    #Add attr
    histories: List[2]


class UserAndReviewsPDSchema(UserBasePDSchema):

    #Add attr
    reviews: List[2]


class AddNewUserPDSchema(UserBasePDSchema):
    pass


class UpdateUserInfoPDSchema(BaseModel):

    telegram_id: Annotated[int, Field]
    name_user: Annotated[str, Field(max_length=500)]
    date_update: datetime


class UpdateUserScore(BaseModel):

    telegram_id: Annotated[int, Field()]
    score: Annotated[int, Field()]