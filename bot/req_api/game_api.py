import requests
from app_settings import tg_settings
from api.backend.schemas.GamePDSchema import GameTranslate
from bot.req_api.game_set import gts

class GameAPI:

    def __init__(self) -> None:
        self.api_url = tg_settings.api_url
        self.session_req: requests.Session = requests.Session()
        self.code: str = "en"

    async def get_words(self) -> GameTranslate:
        """
        Get words
        """

        req = self.session_req.get(self.api_url+"game/random_word/"+self.code)

        if req.status_code == 201:
            data: dict = dict(req.json())
            gts.word = data.get("secret_word")
            gts.translate_word = data.get("translate_in_russo")
            return GameTranslate(secret_word=data.get("secret_word"), translate_in_russo=data.get("translate_in_russo"))
        else:
            return "Наш словарь пуст..."