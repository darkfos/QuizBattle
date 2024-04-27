from fastapi import status, HTTPException


async def http_400_user_not_found():
    """
    Error with not found user
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Пользователь не был найден"
    )

async def http_404_dont_right_login_or_password():
    """
    Error with not right password or login
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Неправильный логин или пароль"
    )

async def http_400_create_error_user():
    """
    Error related to user creation
    """

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось создать пользователя"
    )

async def http_401_auth_user():
    """
    Error with auth user
    """

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось авторизировать, зарегистрировать пользователя"
    )

async def http_409_update_user_info():
    """
    Error with update user info
    """

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Не удалось обновить информацию о пользователе"
    )

async def http_409_delete_user():
    """
    Error with delete user
    """

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Не удалось удалить профиль пользователя"
    )

async def http_400_get_user_info():
    """
    Error with get user info
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Не удалось получить информацию о пользователе"
    )

async def http_400_token_not_found():
    """
    Error with no accept token
    """

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Токен не действителен"
    )