import requests
from bot.req_api.user_set import user_auth_set
from api.backend.schemas.HistoryPDSchema import AddNewHistoryPDSchema
from bot.req_api.user_api import UserApi
from app_settings import tg_settings
from typing import Union, List


class HistoryApi:

    def __init__(self) -> None:
        self.url = tg_settings.api_url
        self.session_req = requests.Session()

    async def create_history(self, new_history: AddNewHistoryPDSchema) -> bool:
        
        try:
            req = self.session_req.post(
                url=self.url+"history/create_history",
                data=new_history.model_dump_json()
            )

            if req.status_code == 201:
                return True
            raise ex
        except Exception as ex:
            await UserApi().generate_new_token()
            new_history.token = user_auth_set.token
            await self.create_history(new_history=new_history)

    async def get_my_histories(self) -> List:
        await UserApi().generate_new_token()
        req = self.session_req.get(
            url=self.url+"history/all_histories",
            params={
                "token": user_auth_set.token
            }
        )

        if req.status_code == 200:
            return req.json()
        else:
            return False