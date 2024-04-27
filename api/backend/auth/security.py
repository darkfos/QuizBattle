from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app_settings import auth_settings
from datetime import timedelta, datetime
from typing import Dict
from api.db.services.UserDbService import UserDatabaseService
from api.backend.schemas.TokenPDSchema import CreateAccessTokenPDSchema
from api.backend.exceptions.user_excception import http_400_user_not_found
from sqlalchemy.ext.asyncio import AsyncSession


class SecurityAPI:

    def __init__(self) -> None:
        self.bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
        self.algorithm: str = auth_settings.algorithm

    async def create_token(self, data_for_token: CreateAccessTokenPDSchema) -> dict:
        """
        Creating access token for user
        """
        
        #Data token
        data: dict = {"tg_id": data_for_token.telegram_id, "user_id": data_for_token.user_id}
        data_for_refresh = data.copy()

        #Token operating time
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.token_time)

        data.update({"exp": expire})
        data_for_refresh.update({"exp": (datetime.utcnow() + timedelta(days=auth_settings.refresh_time))})

        token = jwt.encode(data, key=auth_settings.token_key, algorithm=self.algorithm)
        refresh_token = jwt.encode(data_for_refresh, key=auth_settings.refresh_token_key, algorithm=self.algorithm)

        return {"token": token, "refresh_token": refresh_token}
    
    async def decode_jwt(self, token: str) -> dict:
        """
        Decode jwt token
        """
        
        try:
            data_user: dict = jwt.decode(token=token, key=auth_settings.token_key, algorithms=self.algorithm)
            
            if all(map(lambda x: x != None, data_user.values())):
                return data_user
            return False
        except JWTError as jwt_error:
            return False
        
    async def create_new_token_with_refresh(self, token: str) -> dict:
        """
        Create a new token with refresh token
        """

        try:
            data_user: dict = jwt.decode(token=token, key=auth_settings.refresh_token_key, algorithms=self.algorithm)

            #Create new access token
            expires = datetime.utcnow() + timedelta(minutes=auth_settings.token_time)
            data_user.update({"exp": expires})

            new_token = jwt.encode(data_user, key=auth_settings.token_key, algorithm=self.algorithm)
            
            return {"token": new_token}
        except JWTError as jwt_error:
            return False
        
    async def user_is_created(self, telegram_id: int, session: AsyncSession) -> int:
        """
        Find user
        """

        try:
            
            result = await UserDatabaseService.find_user_by_tg_id(session=session, tg_id=telegram_id)
            
            if result:
                return result
            raise ex
        except Exception as ex:
            await http_400_user_not_found()