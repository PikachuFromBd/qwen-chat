import os
from typing import Optional
from dotenv import load_dotenv
from .exceptions import AuthError


class AuthManager:
    def __init__(self, token: Optional[str] = None, cookie: Optional[str] = None):
        load_dotenv()
        self._token = token or os.getenv("QWEN_AUTH_TOKEN")
        self._cookie = cookie or os.getenv("QWEN_COOKIE")

    def get_token(self) -> str:
        if not self._token:
            raise AuthError("Authentication token not found in .env")
        return f"Bearer {self._token}"

    def get_cookie(self) -> str:
        if self._cookie:
            return self._cookie
        return "x-ap=; acw_tc=; sca=; cna=; _bl_uid=; xlly_s=; token=; tfstk=; isg=; ssxmod_itna=; ssxmod_itna2="
