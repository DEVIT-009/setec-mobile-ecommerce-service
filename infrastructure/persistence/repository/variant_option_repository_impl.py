from typing import Optional, List
from domain.product.ports.variant_option_repository import VariantOptionRepositoryInterface
from domain.product.entity.product import VariantOption
from infrastructure.persistence.mapper.variant_option_persistence_mapper import VariantOptionPersistenceMapper
from infrastructure.persistence.models.product_model import VariantOption as VariantOptionModel


class VariantOptionRepositoryImpl(VariantOptionRepositoryInterface):

    def list_by_variant(self, variant_id: str) -> List[VariantOption]:
        models = VariantOptionModel.objects.filter(
            product_variant_id=variant_id
        ).order_by('name')
        return [VariantOptionPersistenceMapper.from_entity(m) for m in models if m is not None]

    def get_by_id(self, option_id: str) -> Optional[VariantOption]:
        model = VariantOptionModel.objects.filter(id=option_id).first()
        return VariantOptionPersistenceMapper.from_entity(model)

    def save(self, option: VariantOption) -> VariantOption:
        db_instance = (
            VariantOptionModel.objects.filter(pk=option.id).first()
            if option.id else None
        )
        db_instance = VariantOptionPersistenceMapper.to_model(option, db_instance)
        db_instance.save()
        return VariantOptionPersistenceMapper.from_entity(db_instance)

    def delete(self, option_id: str) -> None:
        VariantOptionModel.objects.filter(pk=option_id).delete()

    def exists_name_in_variant(
        self,
        variant_id: str,
        name: str,
        exclude_id: Optional[str] = None,
    ) -> bool:
        qs = VariantOptionModel.objects.filter(
            product_variant_id=variant_id, name=name
        )
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()
