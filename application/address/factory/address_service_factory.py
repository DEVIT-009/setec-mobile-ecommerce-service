from application.address.address_service_facade import AddressServiceFacade
from domain.address.service.address_service import AddressServiceInterface
from infrastructure.persistence.repository.address_repository_impl import AddressRepositoryInterfaceImpl


def address_service_factory() -> AddressServiceInterface:
    repo = AddressRepositoryInterfaceImpl()
    return AddressServiceFacade(repo)
