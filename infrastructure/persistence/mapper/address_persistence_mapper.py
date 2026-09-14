from typing import Optional
from domain.address.entity.address import Address as DomainAddress
from infrastructure.persistence.models.ecom_user_model import UserAddress as UserAddressModel


class AddressPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[UserAddressModel]) -> Optional[DomainAddress]:
        if entity is None:
            return None
        return DomainAddress(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            label=entity.label,
            recipient_name=entity.recipient_name,
            phone_number=entity.phone_number,
            address_line_1=entity.address_line_1,
            address_line_2=entity.address_line_2,
            city=entity.city,
            state=entity.state,
            postal_code=entity.postal_code,
            country_code=entity.country_code,
            latitude=float(entity.latitude) if entity.latitude is not None else None,
            longitude=float(entity.longitude) if entity.longitude is not None else None,
            is_default=entity.is_default,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            deleted_at=entity.deleted_at,
        )

    @staticmethod
    def to_model(domain: DomainAddress, model_instance: Optional[UserAddressModel] = None) -> UserAddressModel:
        model = model_instance or UserAddressModel()
        if domain.user_id:
            model.user_id = domain.user_id
        model.label = domain.label
        model.recipient_name = domain.recipient_name
        model.phone_number = domain.phone_number
        model.address_line_1 = domain.address_line_1
        model.address_line_2 = domain.address_line_2
        model.city = domain.city
        model.state = domain.state
        model.postal_code = domain.postal_code
        model.country_code = domain.country_code
        model.latitude = domain.latitude
        model.longitude = domain.longitude
        model.is_default = domain.is_default
        model.deleted_at = domain.deleted_at
        return model
