from sqlalchemy.ext.asyncio import AsyncSession
from api.db.models.ReviewTable import Review
from api.db.services.ReviewDbService import ReviewDatabaseService
from api.backend.schemas.ReviewPDSchema import *
from api.backend.auth.security import SecurityAPI
from typing import Union, List


app_security: SecurityAPI = SecurityAPI()


class ReviewAPIService:

    @staticmethod
    async def add_new_review(
        session: AsyncSession,
        new_review: AddNewReviewPDSchema
    ) -> ReviewIsCreatedPDSchema:
        """
        Create a new review
        """

        #Get user_id
        user_id: int = ( await app_security.decode_jwt(token=new_review.token) ).get("user_id")

        new_review = Review(
            user_id=user_id,
            message=new_review.message
        )

        is_created: bool = await ReviewDatabaseService.add_record(
            session=session, new_record=new_review
        )

        return ReviewIsCreatedPDSchema(
            is_created=is_created
        )

    @staticmethod
    async def get_all_reviews(
        session: AsyncSession,
        token: str
    ) -> Union[List, List[GetReviewPDSchema]]:
        """
        Get all reviews
        """

        #Get user_id
        user_id: int = ( await app_security.decode_jwt(token=token) ).get("user_id")

        all_reviews = await ReviewDatabaseService.get_all_review_by_user_id(
            session=session,
            user_id=user_id
        )

        if all_reviews:
            return [
                GetReviewPDSchema(
                    message=review[0].message
                )
                    for review in all_reviews
            ]
        else:
            return []