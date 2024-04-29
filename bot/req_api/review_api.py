from api.backend.schemas.ReviewPDSchema import *
import requests
from typing import List
from bot.req_api.user_api import UserApi
from bot.req_api.user_set import user_auth_set
from app_settings import tg_settings


class ReviewAPI:

    def __init__(self) -> None:
        self.url = tg_settings.api_url
        self.session_req: requests.Session = requests.Session()

    async def create_review(self, new_review: AddNewReviewPDSchema) -> bool:
        """
        Create a new review
        """

        #New token
        await UserApi().generate_new_token()

        #Save him
        new_review.token = user_auth_set.token
    
        req = self.session_req.post(
            url=self.url + "review/add_new_review",
            data=new_review.model_dump_json()
        )

        if req.status_code == 201:
            if dict(req.json()).get("is_created") == True:
                return True
            else:
                return False
        else:
            return False