from application.product.product_variant_service_facade import ProductVariantServiceFacade
from domain.product.service.product_variant_service import ProductVariantServiceInterface
from infrastructure.persistence.repository.product_variant_repository_impl import ProductVariantRepositoryImpl


def product_variant_service_factory() -> ProductVariantServiceInterface:
    repo = ProductVariantRepositoryImpl()
    return ProductVariantServiceFacade(repo)
