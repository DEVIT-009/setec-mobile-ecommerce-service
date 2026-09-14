from typing import Dict, Any, Optional
from application.category.factory.category_service_factory import category_service_factory
from application.store.factory.store_service_factory import store_service_factory
from application.product.factory.product_service_factory import product_service_factory


class HomeServiceFacade:

    def __init__(self, cat_service=None, store_service=None, product_service=None):
        self.cat_service = cat_service or category_service_factory()
        self.store_service = store_service or store_service_factory()
        self.product_service = product_service or product_service_factory()

    def get_home(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        categories = self.cat_service.list_active()[:8]
        stores = self.store_service.list_active(page=1, page_size=8)['items']
        products = self.product_service.list_active({}, page=1, page_size=12, user_id=user_id)['items']
        return {
            "featured_categories": categories,
            "featured_stores": stores,
            "featured_products": products,
        }
