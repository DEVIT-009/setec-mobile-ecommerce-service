from dataclasses import dataclass
from typing import Optional


@dataclass
class TagResponse:
    id: Optional[str]
    name: str
    slug: str

    def to_dict(self):
        return self.__dict__
