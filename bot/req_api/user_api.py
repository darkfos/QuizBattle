import requests
from bot.req_api.user_set import UserAuthSet
from api.backend.schemas.UserPDSchema import AddNewUserPDSchema
from app_settings import tg_settings


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