from typing import Dict, Any, List, Optional
from dataclasses import asdict
from domain.address.entity.address import Address
from interface.address.serializer.response.address_response import AddressResponse


class AddressControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any], user_id: Optional[str] = None) -> Address:
        return Address(
            user_id=user_id,
            label=validated_data.get("label"),
            recipient_name=validated_data.get("recipient_name", ""),
            phone_number=validated_data.get("phone_number", ""),
            address_line_1=validated_data.get("address_line_1", ""),
            address_line_2=validated_data.get("address_line_2"),
            city=validated_data.get("city", ""),
            state=validated_data.get("state"),
            postal_code=validated_data.get("postal_code"),
            country_code=validated_data.get("country_code", ""),
            latitude=float(validated_data["latitude"]) if validated_data.get("latitude") is not None else None,
            longitude=float(validated_data["longitude"]) if validated_data.get("longitude") is not None else None,
            is_default=bool(validated_data.get("is_default", False)),
        )

    @staticmethod
    def to_response(address: Address) -> Dict[str, Any]:
        response_dto = AddressResponse(
            id=str(address.id) if address.id else None,
            user_id=str(address.user_id) if address.user_id else None,
            label=address.label,
            recipient_name=address.recipient_name,
            phone_number=address.phone_number,
            address_line_1=address.address_line_1,
            address_line_2=address.address_line_2,
            city=address.city,
            state=address.state,
            postal_code=address.postal_code,
            country_code=address.country_code,
            latitude=address.latitude,
            longitude=address.longitude,
            is_default=address.is_default,
            created_at=address.created_at.isoformat() if address.created_at else None,
            updated_at=address.updated_at.isoformat() if address.updated_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(addresses: List[Address]) -> List[Dict[str, Any]]:
        return [AddressControllerMapper.to_response(a) for a in addresses]

