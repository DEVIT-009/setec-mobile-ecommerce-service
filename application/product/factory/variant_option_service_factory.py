from application.product.variant_option_service_facade import VariantOptionServiceFacade
from domain.product.service.variant_option_service import VariantOptionServiceInterface
from infrastructure.persistence.repository.variant_option_repository_impl import VariantOptionRepositoryImpl


def variant_option_service_factory() -> VariantOptionServiceInterface:
    repo = VariantOptionRepositoryImpl()
    return VariantOptionServiceFacade(repo)
