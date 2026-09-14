from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class HttpBodyErrorResponse:
    type: str
    code: str
    message: str
    error: Optional[str] = None
    bodyRequestError: Optional[Dict[str, str]] = None


@dataclass
class HttpBodyResponse:
    status: int
    message: str
    error: Optional[HttpBodyErrorResponse] = None

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "error": self.error.__dict__ if self.error else None,
        }
