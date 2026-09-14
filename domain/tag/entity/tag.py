from dataclasses import dataclass
from typing import Optional


@dataclass
class Tag:
    id: Optional[str] = None
    name: str = ""
    slug: str = ""
