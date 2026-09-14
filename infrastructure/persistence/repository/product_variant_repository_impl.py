from typing import Optional, List
from django.db import transaction
from django.utils import timezone
from domain.product.ports.product_variant_repository import ProductVariantRepositoryInterface
from domain.product.entity.product import ProductVariant, VariantOption
from infrastructure.persistence.mapper.product_variant_persistence_mapper import ProductVariantPersistenceMapper
from infrastructure.persistence.models.product_model import (
    ProductVariant as ProductVariantModel,
    VariantOption as VariantOptionModel,
)


class ProductVariantRepositoryImpl(ProductVariantRepositoryInterface):

    def list_by_product(self, product_id: str) -> List[ProductVariant]:
        variants = (
            ProductVariantModel.objects
            .filter(product_id=product_id, deleted_at__isnull=True)
            .prefetch_related('options')
            .order_by('created_at')
        )
        return [ProductVariantPersistenceMapper.from_entity(v) for v in variants if v is not None]

    def get_by_id(self, variant_id: str) -> Optional[ProductVariant]:
        model = (
            ProductVariantModel.objects
            .filter(id=variant_id, deleted_at__isnull=True)
            .prefetch_related('options')
            .first()
        )
        return ProductVariantPersistenceMapper.from_entity(model)

    @transaction.atomic
    def save(self, variant: ProductVariant, actor_id: Optional[str] = None) -> ProductVariant:
        db_instance = (
            ProductVariantModel.objects.filter(pk=variant.id).first()
            if variant.id else None
        )
        is_new = db_instance is None
        db_instance = ProductVariantPersistenceMapper.to_model(variant, db_instance)
        if actor_id:
            if is_new:
                db_instance.created_by_id = actor_id
            db_instance.updated_by_id = actor_id
        db_instance.save()

        # Sync options: replace all existing options with the new set
        if variant.options is not None:
            db_instance.options.all().delete()
            for opt in variant.options:
                VariantOptionModel.objects.create(
                    product_variant=db_instance,
                    name=opt.name,
                    value=opt.value,
                )

        # Re-fetch with options to return a fully hydrated entity
        db_instance.refresh_from_db()
        return ProductVariantPersistenceMapper.from_entity(
            ProductVariantModel.objects
            .filter(pk=db_instance.pk)
            .prefetch_related('options')
            .first()
        )

    def soft_delete(self, variant_id: str, actor_id: Optional[str] = None) -> None:
        update_fields = {'deleted_at': timezone.now()}
        if actor_id:
            update_fields['deleted_by_id'] = actor_id
        ProductVariantModel.objects.filter(pk=variant_id, deleted_at__isnull=True).update(**update_fields)

    def exists_sku(self, sku: str, exclude_id: Optional[str] = None) -> bool:
        qs = ProductVariantModel.objects.filter(sku=sku, deleted_at__isnull=True)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()
