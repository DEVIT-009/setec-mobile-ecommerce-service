from typing import Optional, List
from domain.product.entity.product import ProductVariant as DomainProductVariant, VariantOption as DomainVariantOption
from infrastructure.persistence.models.product_model import (
    ProductVariant as ProductVariantModel,
    VariantOption as VariantOptionModel,
)


class ProductVariantPersistenceMapper:

    @staticmethod
    def variant_option_from_entity(entity: Optional[VariantOptionModel]) -> Optional[DomainVariantOption]:
        if entity is None:
            return None
        return DomainVariantOption(
            id=str(entity.id),
            variant_id=str(entity.product_variant_id) if entity.product_variant_id else None,
            name=entity.name,
            value=entity.value,
        )


    @staticmethod
    def from_entity(entity: Optional[ProductVariantModel]) -> Optional[DomainProductVariant]:
        if entity is None:
            return None
        options = []
        if hasattr(entity, 'options'):
            options = [
                ProductVariantPersistenceMapper.variant_option_from_entity(o)
                for o in entity.options.all()
            ]
        return DomainProductVariant(
            id=str(entity.id),
            product_id=str(entity.product_id) if entity.product_id else None,
            sku=entity.sku,
            name=entity.name,
            price=float(entity.price) if entity.price is not None else None,
            stock_quantity=entity.stock_quantity,
            status=entity.status,
            options=[opt for opt in options if opt is not None],
        )

    @staticmethod
    def to_model(
        domain: DomainProductVariant,
        model_instance: Optional[ProductVariantModel] = None,
    ) -> ProductVariantModel:
        model = model_instance or ProductVariantModel()
        if domain.product_id:
            model.product_id = domain.product_id
        model.sku = domain.sku
        model.name = domain.name
        model.price = domain.price
        model.stock_quantity = domain.stock_quantity
        model.status = domain.status
        return model
