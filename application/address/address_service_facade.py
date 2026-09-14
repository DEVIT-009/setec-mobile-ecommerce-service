from typing import Dict, Any, List, Optional
from domain.address.ports.address_repository import AddressRepositoryInterface
from domain.address.service.address_service import AddressServiceInterface
from domain.address.entity.address import Address
from domain.address.exception.address_exception import AddressException
from interface.address.serializer.mapper.address_controller_mapper import AddressControllerMapper


class AddressServiceFacade(AddressServiceInterface):

    def __init__(self, repo: AddressRepositoryInterface):
        self.repo = repo

    def list(self, user_id: str) -> List[Dict[str, Any]]:
        addresses = self.repo.list_by_user(user_id)
        return AddressControllerMapper.to_list_response(addresses)

    def create(self, user_id: str, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]:
        country_code = data.get('country_code', '')
        if len(country_code) != 2:
            raise AddressException.invalid_country_code()

        address = AddressControllerMapper.from_request(data, user_id=user_id)
        if address.is_default:
            self.repo.clear_default(user_id)

        saved = self.repo.create(address, actor_id=actor_id)
        return AddressControllerMapper.to_response(saved)

    def get(self, address_id: str, user_id: str) -> Dict[str, Any]:
        address = self.repo.get_by_id(address_id, user_id=user_id)
        if not address:
            raise AddressException.not_found()
        return AddressControllerMapper.to_response(address)

    def update(self, address_id: str, user_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        existing = self.repo.get_by_id(address_id, user_id=user_id)
        if not existing:
            raise AddressException.not_found()

        if 'country_code' in data and len(data['country_code']) != 2:
            raise AddressException.invalid_country_code()

        fields = [
            'label', 'recipient_name', 'phone_number', 'address_line_1',
            'address_line_2', 'city', 'state', 'postal_code', 'country_code'
        ]
        for field in fields:
            if field in data or not partial:
                if field in data:
                    setattr(existing, field, data[field])

        if 'latitude' in data or not partial:
            if 'latitude' in data:
                existing.latitude = float(data['latitude']) if data['latitude'] is not None else None
        if 'longitude' in data or not partial:
            if 'longitude' in data:
                existing.longitude = float(data['longitude']) if data['longitude'] is not None else None
        if 'is_default' in data or not partial:
            if 'is_default' in data:
                if data['is_default']:
                    self.repo.clear_default(user_id)
                existing.is_default = bool(data['is_default'])

        saved = self.repo.update(existing, actor_id=actor_id)
        return AddressControllerMapper.to_response(saved)

    def delete(self, address_id: str, user_id: str, actor_id: Optional[str] = None) -> None:
        self.soft_delete(address_id, user_id, actor_id=actor_id)

    def soft_delete(self, address_id: str, user_id: str, actor_id: Optional[str] = None) -> None:
        existing = self.repo.get_by_id(address_id, user_id=user_id)
        if not existing:
            raise AddressException.not_found()
        self.repo.soft_delete(address_id, user_id=user_id, actor_id=actor_id)

    def set_default(self, address_id: str, user_id: str, actor_id: Optional[str] = None) -> Dict[str, Any]:
        existing = self.repo.get_by_id(address_id, user_id=user_id)
        if not existing:
            raise AddressException.not_found()
        self.repo.clear_default(user_id)
        existing.is_default = True
        saved = self.repo.update(existing, actor_id=actor_id)
        return AddressControllerMapper.to_response(saved)
