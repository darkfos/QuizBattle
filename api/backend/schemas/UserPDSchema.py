from pydantic import Field, BaseModel
from typing import Annotated, Union, List
from datetime import datetime
from api.backend.schemas.HistoryPDSchema import GetHistoryPDSchema
from api.backend.schemas.ReviewPDSchema import GetReviewPDSchema


class UserBasePDSchema(BaseModel):
    
    name_user: Annotated[str, Field(max_length=500)]
    score: Annotated[int, Field()]
    date_create: datetime = Field(default=datetime.now().date())
    date_update: datetime = Field(default=datetime.now().date())


class UserFullInformationPDSchema(UserBasePDSchema):

    reviews: List[GetReviewPDSchema]
    histories: List[GetHistoryPDSchema]


class UserAndHistoryPDSchema(UserBasePDSchema):

    #Add attr
    histories: List[GetHistoryPDSchema]


class UserAndReviewsPDSchema(UserBasePDSchema):

    #Add attr
    reviews: List[GetReviewPDSchema]


class AddNewUserPDSchema(UserBasePDSchema):
    
    #Add attr
    telegram_id: Annotated[int, Field()]


class UpdateUserInfoPDSchema(BaseModel):

    token: Annotated[str, Field]
    name_user: Annotated[str, Field(max_length=500)]
    date_update: datetime


class UpdateUserScorePDSchema(BaseModel):

    token: Annotated[int, Field()]
    score: Annotated[int, Field()]


class UserIsCreatedPDSchema(BaseModel):

    is_created: bool


class UserIsUpdated(BaseModel):

    is_updated: bool


class UserIsDeletedPDSchema(BaseModel):

    is_deleted: bool