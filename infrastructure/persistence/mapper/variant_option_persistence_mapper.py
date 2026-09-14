from typing import Optional
from domain.product.entity.product import VariantOption as DomainVariantOption
from infrastructure.persistence.models.product_model import VariantOption as VariantOptionModel


class VariantOptionPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[VariantOptionModel]) -> Optional[DomainVariantOption]:
        if entity is None:
            return None
        return DomainVariantOption(
            id=str(entity.id),
            variant_id=str(entity.product_variant_id) if entity.product_variant_id else None,
            name=entity.name,
            value=entity.value,
        )

    @staticmethod
    def to_model(
        domain: DomainVariantOption,
        model_instance: Optional[VariantOptionModel] = None,
    ) -> VariantOptionModel:
        model = model_instance or VariantOptionModel()
        if domain.variant_id:
            model.product_variant_id = domain.variant_id
        model.name = domain.name
        model.value = domain.value
        return model
