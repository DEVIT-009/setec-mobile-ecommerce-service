from application.shipment.shipment_service_facade import ShipmentServiceFacade
from domain.shipment.service.shipment_service import ShipmentServiceInterface
from infrastructure.persistence.repository.shipment_repository_impl import ShipmentRepositoryInterfaceImpl


def shipment_service_factory() -> ShipmentServiceInterface:
    repo = ShipmentRepositoryInterfaceImpl()
    return ShipmentServiceFacade(repo)
