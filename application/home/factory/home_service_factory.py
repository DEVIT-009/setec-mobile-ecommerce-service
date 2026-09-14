from application.home.home_service_facade import HomeServiceFacade


def home_service_factory() -> HomeServiceFacade:
    return HomeServiceFacade()
