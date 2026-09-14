from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressResponse:
    id: Optional[str]
    recipient_name: str
    phone_number: str
    address_line_1: str
    city: str
    country_code: str
    user_id: Optional[str] = None
    label: Optional[str] = None
    address_line_2: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self):
        return self.__dict__
