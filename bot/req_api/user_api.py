import requests
from bot.req_api.user_set import user_auth_set
from api.backend.schemas.UserPDSchema import AddNewUserPDSchema, UpdateUserScorePDSchema, UpdateUserGameCountPDSchema
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
            data=user_data.model_dump_json()
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
        cookie_result = dict(result.cookies)
        if result.status_code == 200:
            res = dict(result.json())
            user_auth_set.token = res.get("token")
            user_auth_set.refresh_token = cookie_result.get("refresh_token")
        else:
            return False
        
    async def generate_new_token(self) -> None:
        """
        Generate new token with help refresh_token
        """

        result = self.session_req.post(
            url=self.url+"auth/refresh_token",
            params={
                "token": user_auth_set.refresh_token
            }
        )


        if result.status_code == 200:
            user_auth_set.token = dict(result.json()).get("token")
        else:
            return False
    
    async def get_user_info(self) -> None:
        """
        Get user info
        """

        try:
            result = self.session_req.get(
                url=self.url+"user/about_me",
                params={"token": user_auth_set.token}
            )

            if result.status_code == 200:
                return dict(result.json())
            else:
                raise ex
            
        except Exception as ex:
            await self.generate_new_token()
            await self.get_user_info()
    

    async def get_full_user_info(self) -> None:
        """
        Get full user info
        """

        try:
            result = self.session_req.get(
                url=self.url+"user/about_me/full-information",
                params={"token": user_auth_set.token}
            )
            
            if result.status_code == 200:
                return dict(result.json())
            else:
                raise ex
            
        except Exception as ex:
            await self.generate_new_token()
            await self.get_full_user_info()

    async def update_user_score(self, score: int) -> None:
        """
        Update user score
        """

        try:
            result = self.session_req.patch(
                url=self.url+"user/update_user_score",
                data=UpdateUserScorePDSchema(
                    token=user_auth_set.token,
                    score=score
                ).model_dump_json()
            )


            if result.status_code == 202:
                res = dict(result.json())

                if res.get("is_updated") == True:
                    pass
            else:
                raise ex
                
        except Exception as ex:
            res_generate = await self.generate_new_token()
            if res_generate is False:
                pass
            else:
                await self.update_user_score(score=score)

    async def update_user_game_count(self, game_count: int) -> None:
        try:
            result = self.session_req.patch(
                url=self.url+"user/update_user_game_count",
                data=UpdateUserGameCountPDSchema(
                    token=user_auth_set.token,
                    game_count=game_count
                ).model_dump_json()
            )


            if result.status_code == 202:
                res = dict(result.json())

                if res.get("is_updated") == True:
                    pass
            else:
                raise ex
                
        except Exception as ex:
            res_generate = await self.generate_new_token()
            if res_generate is False:
                pass
            else:
                await self.update_user_score(game_count=game_count)