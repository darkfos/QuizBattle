from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.backend.schemas.ReviewPDSchema import *
from api.backend.services.ReviewService import ReviewAPIService
from api.db.db_engine import db_worker
from typing import List, Annotated


review_router: APIRouter = APIRouter(
    prefix="/review",
    tags=["Review"]
)


@review_router.post("/add_new_review",
                    status_code=status.HTTP_201_CREATED,
                    response_model=ReviewIsCreatedPDSchema
                    )
async def create_new_review_by_user(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    new_review: AddNewReviewPDSchema   
) -> ReviewIsCreatedPDSchema:
    """
    Create a new review
    """

    return await ReviewAPIService.add_new_review(session=session, new_review=new_review)


@review_router.get("/all_review_by_user",
                   status_code=status.HTTP_200_OK,
                   response_model=Union[List, List[GetReviewPDSchema]])
async def get_all_review_by_user(
    session: Annotated[AsyncSession, Depends(db_worker.get_session)],
    token: str
) -> Union[List, List[GetReviewPDSchema]]:
    """
    Get all review by user
    """

    return await ReviewAPIService.get_all_reviews(session=session, token=token)