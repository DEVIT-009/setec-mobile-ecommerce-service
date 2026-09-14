from application.user.user_service_facade import UserServiceFacade
from domain.user.service.user_service import UserServiceInterface
from infrastructure.persistence.repository.user_repository_impl import UserRepositoryInterfaceImpl
from infrastructure.persistence.repository.address_repository_impl import AddressRepositoryInterfaceImpl


def user_service_factory() -> UserServiceInterface:
    user_repo = UserRepositoryInterfaceImpl()
    address_repo = AddressRepositoryInterfaceImpl()
    return UserServiceFacade(user_repo=user_repo, address_repo=address_repo)
