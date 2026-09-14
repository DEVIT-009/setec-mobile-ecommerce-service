from typing import Optional, List
from domain.product.entity.product import Product as DomainProduct, ProductImage as DomainProductImage, ProductVariant as DomainProductVariant, VariantOption as DomainVariantOption, Tag as DomainTag
from infrastructure.persistence.models.product_model import (
    Product as ProductModel,
    ProductImage as ProductImageModel,
    ProductVariant as ProductVariantModel,
    VariantOption as VariantOptionModel,
    Tag as TagModel,
)


class ProductPersistenceMapper:

    @staticmethod
    def image_from_entity(entity: Optional[ProductImageModel]) -> Optional[DomainProductImage]:
        if entity is None:
            return None
        return DomainProductImage(
            id=str(entity.id),
            product_id=str(entity.product_id) if entity.product_id else None,
            image_url=entity.image_url,
            alt_text=entity.alt_text,
            sort_order=entity.sort_order,
            is_primary=entity.is_primary,
        )

    @staticmethod
    def image_to_model(domain: DomainProductImage, model_instance: Optional[ProductImageModel] = None) -> ProductImageModel:
        model = model_instance or ProductImageModel()
        model.image_url = domain.image_url
        model.alt_text = domain.alt_text
        model.sort_order = domain.sort_order
        model.is_primary = domain.is_primary
        if domain.product_id:
            model.product_id = domain.product_id
        return model

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
    def variant_from_entity(entity: Optional[ProductVariantModel]) -> Optional[DomainProductVariant]:
        if entity is None:
            return None
        options = []
        if hasattr(entity, 'options'):
            options = [ProductPersistenceMapper.variant_option_from_entity(o) for o in entity.options.all()]
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
    def tag_from_entity(entity: Optional[TagModel]) -> Optional[DomainTag]:
        if entity is None:
            return None
        return DomainTag(
            id=str(entity.id),
            name=entity.name,
            slug=entity.slug,
        )

    @staticmethod
    def from_entity(entity: Optional[ProductModel]) -> Optional[DomainProduct]:
        if entity is None:
            return None
        
        domain = DomainProduct(
            id=str(entity.id),
            store_id=str(entity.store_id) if entity.store_id else None,
            store_name=entity.store.name if getattr(entity, 'store', None) else None,
            store_slug=entity.store.slug if getattr(entity, 'store', None) else None,
            category_id=str(entity.category_id) if entity.category_id else None,
            category_name=entity.category.name if getattr(entity, 'category', None) else None,
            name=entity.name,
            slug=entity.slug,
            description=entity.description,
            base_price=float(entity.base_price) if entity.base_price is not None else 0.0,
            compare_at_price=float(entity.compare_at_price) if entity.compare_at_price is not None else None,
            currency=entity.currency,
            sku=entity.sku,
            status=entity.status,
            rating_average=float(entity.rating_average) if entity.rating_average is not None else 0.0,
            rating_count=entity.rating_count,
            sold_count=entity.sold_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )
        return domain

    @staticmethod
    def to_model(domain: DomainProduct, model_instance: Optional[ProductModel] = None) -> ProductModel:
        model = model_instance or ProductModel()
        if domain.store_id:
            model.store_id = domain.store_id
        if domain.category_id:
            model.category_id = domain.category_id
        model.name = domain.name
        model.slug = domain.slug
        model.description = domain.description
        model.base_price = domain.base_price
        model.compare_at_price = domain.compare_at_price
        model.currency = domain.currency
        model.sku = domain.sku
        model.status = domain.status
        return model
