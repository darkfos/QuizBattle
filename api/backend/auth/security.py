from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app_settings import auth_settings
from datetime import timedelta, datetime
from typing import Dict


class SecurityAPI:

    def __init__(self) -> None:
        self.bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
        self.algorithm: str = auth_settings.algorithm

    def create_token(self, tg_id: int, user_id: int) -> dict:
        """
        Creating access token for user
        """
        
        #Data token
        data: dict = {"tg_id": tg_id, "user_id": user_id}
        data_for_refresh = data.copy()

        #Token operating time
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.token_time)

        data.update({"exp": expire})
        data_for_refresh.update({"exp": (datetime.utcnow() + timedelta(days=auth_settings.refresh_time))})

        token = jwt.encode(data, key=auth_settings.token_key, algorithm=self.algorithm)
        refresh_token = jwt.encode(data_for_refresh, key=auth_settings.refresh_token_key, algorithm=self.algorithm)

        return {"token": token, "refresh_token": refresh_token}
    
    def decode_jwt(self, token: str) -> dict:
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
        
    def create_new_token_with_refresh(self, token: str) -> dict:
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