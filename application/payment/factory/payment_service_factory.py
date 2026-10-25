from application.payment.payment_service_facade import PaymentServiceFacade
from domain.payment.service.payment_service import PaymentServiceInterface
from infrastructure.persistence.repository.payment_repository_impl import PaymentRepositoryInterfaceImpl


def payment_service_factory() -> PaymentServiceInterface:
    return PaymentServiceFacade(PaymentRepositoryInterfaceImpl())
