from fastapi import status, HTTPException


async def http_409_error_create_history():
    """
    Error with create history by user
    """

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Не удалось создать историю"
    )

async def http_404_error_get_history():
    """
    Error with get history
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Не удалось получить запись об истории"
    )

async def http_404_error_get_all_histories():
    """
    Error with get all histories
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Не удалось получить записи об всех историях"
    )

async def http_409_error_delete_history():
    """
    Error with delete hisotry
    """

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Не удалось удалить запись об истории"
    )