from typing import Optional, Dict, Any, List
from domain.product.entity.product import ProductVariant
from domain.product.ports.product_variant_repository import ProductVariantRepositoryInterface
from domain.product.service.product_variant_service import ProductVariantServiceInterface
from domain.product.exception.product_exception import ProductException
from interface.product.serializer.mapper.product_variant_controller import ProductVariantControllerMapper


class ProductVariantServiceFacade(ProductVariantServiceInterface):

    def __init__(self, repo: ProductVariantRepositoryInterface):
        self.repo = repo

    def list_by_product(self, product_id: str) -> List[Dict[str, Any]]:
        variants = self.repo.list_by_product(product_id)
        return ProductVariantControllerMapper.to_list_response(variants)

    def get_by_id(self, variant_id: str) -> Dict[str, Any]:
        variant = self.repo.get_by_id(variant_id)
        if not variant:
            raise ProductException.not_found("Product variant not found")
        return ProductVariantControllerMapper.to_detail_response(variant)

    def create(self, data: Dict[str, Any], actor_id: Optional[str] = None) -> Dict[str, Any]:
        sku = data.get('sku')
        if sku and self.repo.exists_sku(sku):
            raise ProductException.already_exists(f"A variant with SKU '{sku}' already exists")

        variant = ProductVariantControllerMapper.from_request(data)
        saved = self.repo.save(variant, actor_id=actor_id)
        return ProductVariantControllerMapper.to_detail_response(saved)

    def update(
        self,
        variant_id: str,
        data: Dict[str, Any],
        actor_id: Optional[str] = None,
        partial: bool = False,
    ) -> Dict[str, Any]:
        existing = self.repo.get_by_id(variant_id)
        if not existing:
            raise ProductException.not_found("Product variant not found")

        sku = data.get('sku')
        if sku and sku != existing.sku and self.repo.exists_sku(sku, exclude_id=existing.id):
            raise ProductException.already_exists(f"A variant with SKU '{sku}' already exists")

        if not partial or 'name' in data:
            existing.name = data.get('name', existing.name)
        if not partial or 'sku' in data:
            existing.sku = data.get('sku', existing.sku)
        if not partial or 'price' in data:
            existing.price = float(data['price']) if data.get('price') is not None else (None if 'price' in data else existing.price)
        if not partial or 'stock_quantity' in data:
            existing.stock_quantity = data.get('stock_quantity', existing.stock_quantity)
        if not partial or 'status' in data:
            existing.status = data.get('status', existing.status)
        if not partial or 'options' in data:
            if 'options' in data:
                from domain.product.entity.product import VariantOption
                existing.options = [VariantOption(name=o['name'], value=o['value']) for o in data['options']]

        saved = self.repo.save(existing, actor_id=actor_id)
        return ProductVariantControllerMapper.to_detail_response(saved)

    def soft_delete(self, variant_id: str, actor_id: Optional[str] = None) -> None:
        existing = self.repo.get_by_id(variant_id)
        if not existing:
            raise ProductException.not_found("Product variant not found")
        self.repo.soft_delete(existing.id, actor_id=actor_id)
