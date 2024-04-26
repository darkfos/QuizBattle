from fastapi import status, HTTPException


async def http_409_create_review():
    """
    Error with create review by user
    """

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Не удалось создать отзыв"
    )

async def http_404_get_all_reviews():
    """
    Error with get all reviews
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Не удалось получить все отзывы"
    )

async def http_404_get_review():
    """
    Error with get review
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Не удалось получить отзыв"
    )