import requests
from bot.req_api.user_set import user_auth_set
from api.backend.schemas.UserPDSchema import AddNewUserPDSchema
from app_settings import tg_settings
from typing import Union


class UserApi:

    def __init__(self) -> None:
        self.url = tg_settings.api_url
        self.session_req: requests.Session = requests.Session()

    async def register_user(self, user_data: AddNewUserPDSchema) -> bool:
        """
            Register a new user
        """

        result = self.session_req.post(
            url=self.url+"user/create_user",
            data=user_data
            )
        
        if result.status_code == 201:
            return True
        else:
            return False
        
    async def create_access_token(self, telegram_id: int) -> None:
        """
            Creating a new token
        """
        
        result = self.session_req.post(
            url=self.url+f"auth/create_token/{telegram_id}"
        )
        #cookie
        cookie_result = result.cookies

        if result.status_code == 201:
            res = dict(result.json())
            user_auth_set.token = res.get("token")
            user_auth_set.refresh_token = cookie_result.get("refresh_token")
        else:
            return False
        
    async def generate_new_token(self, token: str) -> None
        """
        Generate new token with help refresh_token
        """

        result = self.session_req.post(
            url=self.url+"auth/refresh_token",
            params={
                "token": token
            }
        )

        if result.status_code == 200:
            user_auth_set.token = dict(result.json()).get("token")
        else:
            return "Не удалось получить новый token"