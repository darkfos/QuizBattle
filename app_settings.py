from typing import Final


class DatabaseSettings:
    
    def __init__(self) -> None:
        self.__url_db: str = ...
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
        self.__token: str = ...

    @property
    def token(self) -> str: return self.__token


class AuthSettings:

    def __init__(self) -> None:
        self.__key_auth_for_token: str = ...
        self.__key_auth_for_refresh_token: str = ...

    @property
    def token_key(self) -> str: return self.__key_auth_for_token

    @property
    def refresh_token_key(self) -> str: return self.__key_auth_for_refresh_token