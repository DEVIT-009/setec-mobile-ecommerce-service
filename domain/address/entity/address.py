from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Address:
    id: Optional[str] = None
    user_id: Optional[str] = None
    label: Optional[str] = None
    recipient_name: str = ""
    phone_number: str = ""
    address_line_1: str = ""
    address_line_2: Optional[str] = None
    city: str = ""
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
