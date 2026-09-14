from typing import Optional, Dict, Any, List
from domain.product.entity.product import VariantOption
from domain.product.ports.variant_option_repository import VariantOptionRepositoryInterface
from domain.product.service.variant_option_service import VariantOptionServiceInterface
from domain.product.exception.product_exception import ProductException
from interface.product.serializer.mapper.variant_option_controller import VariantOptionControllerMapper


class VariantOptionServiceFacade(VariantOptionServiceInterface):

    def __init__(self, repo: VariantOptionRepositoryInterface):
        self.repo = repo

    def list_by_variant(self, variant_id: str) -> List[Dict[str, Any]]:
        options = self.repo.list_by_variant(variant_id)
        return VariantOptionControllerMapper.to_list_response(options)

    def get_by_id(self, option_id: str) -> Dict[str, Any]:
        option = self.repo.get_by_id(option_id)
        if not option:
            raise ProductException.not_found("Variant option not found")
        return VariantOptionControllerMapper.to_detail_response(option)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        variant_id = str(data.get('variant_id', ''))
        name = data.get('name', '')
        if self.repo.exists_name_in_variant(variant_id, name):
            raise ProductException.already_exists(
                f"An option with name '{name}' already exists for this variant"
            )
        option = VariantOptionControllerMapper.from_request(data)
        saved = self.repo.save(option)
        return VariantOptionControllerMapper.to_detail_response(saved)

    def update(
        self,
        option_id: str,
        data: Dict[str, Any],
        partial: bool = False,
    ) -> Dict[str, Any]:
        existing = self.repo.get_by_id(option_id)
        if not existing:
            raise ProductException.not_found("Variant option not found")

        new_name = data.get('name', existing.name)
        if new_name != existing.name and self.repo.exists_name_in_variant(
            existing.variant_id, new_name, exclude_id=option_id
        ):
            raise ProductException.already_exists(
                f"An option with name '{new_name}' already exists for this variant"
            )

        if not partial or 'name' in data:
            existing.name = data.get('name', existing.name)
        if not partial or 'value' in data:
            existing.value = data.get('value', existing.value)

        saved = self.repo.save(existing)
        return VariantOptionControllerMapper.to_detail_response(saved)

    def delete(self, option_id: str) -> None:
        existing = self.repo.get_by_id(option_id)
        if not existing:
            raise ProductException.not_found("Variant option not found")
        self.repo.delete(option_id)
