from dataclasses import dataclass
from typing import Optional


@dataclass
class VariantOptionDetailResponse:
    id: Optional[str]
    variant_id: Optional[str]
    name: str
    value: str

    def to_dict(self):
        return self.__dict__
