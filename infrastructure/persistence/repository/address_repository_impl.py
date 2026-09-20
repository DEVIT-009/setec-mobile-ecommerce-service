from typing import List, Optional
from django.utils import timezone
from domain.address.ports.address_repository import AddressRepositoryInterface
from domain.address.entity.address import Address
from domain.address.exception.address_exception import AddressException
from infrastructure.persistence.mapper.address_persistence_mapper import AddressPersistenceMapper
from infrastructure.persistence.models.ecom_user_model import UserAddress as UserAddressModel


class AddressRepositoryInterfaceImpl(AddressRepositoryInterface):

    def list_by_user(self, user_id: str) -> List[Address]:
        addresses = UserAddressModel.objects.filter(
            user_id=user_id,
            deleted_at__isnull=True,
        ).order_by('-is_default', '-created_at')
        return [AddressPersistenceMapper.from_entity(a) for a in addresses if a is not None]

    def get_by_id(self, address_id: str, user_id: Optional[str] = None) -> Optional[Address]:
        qs = UserAddressModel.objects.filter(id=address_id, deleted_at__isnull=True)
        if user_id is not None:
            qs = qs.filter(user_id=user_id)
        address = qs.first()
        if not address:
            return None
        return AddressPersistenceMapper.from_entity(address)

    def create(self, address: Address, actor_id: Optional[str] = None) -> Address:
        model = AddressPersistenceMapper.to_model(address)
        if actor_id:
            model.created_by_id = actor_id
            model.updated_by_id = actor_id
        model.save()
        return AddressPersistenceMapper.from_entity(model)

    def update(self, address: Address, actor_id: Optional[str] = None) -> Address:
        if not address.id:
            raise AddressException.not_found()
        model = UserAddressModel.objects.filter(id=address.id, deleted_at__isnull=True).first()
        if not model:
            raise AddressException.not_found()
        model = AddressPersistenceMapper.to_model(address, model)
        if actor_id:
            model.updated_by_id = actor_id
        model.save()
        return AddressPersistenceMapper.from_entity(model)

    def soft_delete(self, address_id: str, user_id: Optional[str] = None, actor_id: Optional[str] = None) -> None:
        qs = UserAddressModel.objects.filter(id=address_id, deleted_at__isnull=True)
        if user_id is not None:
            qs = qs.filter(user_id=user_id)
        model = qs.first()
        if not model:
            raise AddressException.not_found()
        model.deleted_at = timezone.now()
        if actor_id:
            model.deleted_by_id = actor_id
        model.save()

    def clear_default(self, user_id: str) -> None:
        UserAddressModel.objects.filter(user_id=user_id, deleted_at__isnull=True).update(is_default=False)

    def save(self, address: Address, actor_id: Optional[str] = None) -> Address:
        """Backward-compatible save method."""
        if address.id and UserAddressModel.objects.filter(id=address.id, deleted_at__isnull=True).exists():
            return self.update(address, actor_id=actor_id)
        return self.create(address, actor_id=actor_id)
