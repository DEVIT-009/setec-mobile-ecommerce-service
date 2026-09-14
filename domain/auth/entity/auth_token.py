from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthToken:
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
