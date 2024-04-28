from pydantic import Field, BaseModel
from typing import Annotated, Union, List


class ReviewBasePDSchema(BaseModel):

    message: Annotated[str, Field()]


class AddNewReviewPDSchema(ReviewBasePDSchema):
    
    #Add attr
    token: str


class GetReviewPDSchema(ReviewBasePDSchema):
    pass


class ReviewIsCreatedPDSchema(BaseModel):

    is_created: bool