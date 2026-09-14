from application.order.order_service_facade import OrderServiceFacade
from domain.order.service.order_service import OrderServiceInterface
from infrastructure.persistence.repository.order_repository_impl import OrderRepositoryInterfaceImpl


def order_service_factory() -> OrderServiceInterface:
    repo = OrderRepositoryInterfaceImpl()
    return OrderServiceFacade(repo)
