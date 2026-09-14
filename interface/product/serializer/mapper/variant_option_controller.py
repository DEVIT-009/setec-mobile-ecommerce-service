from typing import List, Dict, Any
from dataclasses import asdict
from domain.product.entity.product import VariantOption
from interface.product.serializer.response.variant_option_response import VariantOptionDetailResponse


class VariantOptionControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any]) -> VariantOption:
        """Convert validated request dict → Domain Entity."""
        return VariantOption(
            variant_id=str(validated_data.get('variant_id', '')),
            name=validated_data.get('name', ''),
            value=validated_data.get('value', ''),
        )

    @staticmethod
    def to_detail_response(o: VariantOption) -> Dict[str, Any]:
        response_dto = VariantOptionDetailResponse(
            id=str(o.id) if o.id else None,
            variant_id=str(o.variant_id) if o.variant_id else None,
            name=o.name,
            value=o.value,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(options: List[VariantOption]) -> List[Dict[str, Any]]:
        return [VariantOptionControllerMapper.to_detail_response(o) for o in options]
