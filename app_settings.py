from typing import Final
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class DatabaseSettings:
    
    def __init__(self) -> None:
        self.__url_db: str = getenv("DATABASE_URL") + getenv("DATABASE_USERNAME") + ":" + getenv("DATABASE_PASSWORD") + "@" + getenv("DATABASE_URL") + ":" + getenv("DATABASE_PORT") + "/" + getenv("DATABASE_NAME")
        self.__echo: bool = True

    @property
    def url_db(self) -> str: return self.__url_db

    @property
    def echo(self) -> bool: return self.echo

    @echo.setter
    def echo(self, new_param_for_echo: bool):
        self.__echo = new_param_for_echo


class TelegramSettings:

    def __init__(self) -> None:
        self.__token: str = getenv("TELEGRAM_BOT_TOKEN")

    @property
    def token(self) -> str: return self.__token


class AuthSettings:

    def __init__(self) -> None:
        self.__key_auth_for_token: str = getenv("TOKEN_KEY")
        self.__key_auth_for_refresh_token: str = getenv("REFRESH_TOKEN_KEY")

    @property
    def token_key(self) -> str: return self.__key_auth_for_token

    @property
    def refresh_token_key(self) -> str: return self.__key_auth_for_refresh_token


#Initializating settings
tg_settings: TelegramSettings = TelegramSettings()
db_settings: DatabaseSettings = DatabaseSettings()
auth_settings: AuthSettings = AuthSettings()