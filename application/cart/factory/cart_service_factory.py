from application.cart.cart_service_facade import CartServiceFacade
from domain.cart.service.cart_service import CartServiceInterface
from infrastructure.persistence.repository.cart_repository_impl import CartRepositoryInterfaceImpl
from infrastructure.persistence.repository.product_repository_impl import ProductRepositoryInterfaceImpl


def cart_service_factory() -> CartServiceInterface:
    cart_repo = CartRepositoryInterfaceImpl()
    product_repo = ProductRepositoryInterfaceImpl()
    return CartServiceFacade(cart_repo=cart_repo, product_repo=product_repo)
