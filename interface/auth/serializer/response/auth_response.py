from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AuthTokenResponse:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    user: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return self.__dict__


@dataclass
class AuthMessageResponse:
    message: str

    def to_dict(self):
        return self.__dict__
