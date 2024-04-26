from pydantic import Field, BaseModel
from typing import Annotated, Union, List


class ReviewBasePDSchema(BaseModel):

    message: Annotated[str, Field()]


class AddNewReviewPDSchema(ReviewBasePDSchema):
    
    #Add attr
    telegram_id: int


class GetReviewPDSchema(ReviewBasePDSchema):
    pass