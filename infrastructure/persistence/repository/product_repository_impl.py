from typing import Optional, Tuple, List
from django.utils import timezone
from domain.product.ports.product_repository import ProductRepositoryInterface
from domain.product.entity.product import Product, ProductImage, ProductVariant, Tag
from infrastructure.persistence.mapper.product_persistence_mapper import ProductPersistenceMapper
from infrastructure.persistence.models.product_model import (
    Product as ProductModel,
    ProductImage as ProductImageModel,
    ProductVariant as ProductVariantModel,
    Tag as TagModel,
)
from infrastructure.persistence.models.favorite_model import Favorite as FavoriteModel


class ProductRepositoryInterfaceImpl(ProductRepositoryInterface):

    def list_active(self, filters: dict, page: int, page_size: int, user_id: Optional[str] = None) -> Tuple[List[Product], int]:
        qs = ProductModel.objects.filter(status='active', deleted_at__isnull=True).select_related('store', 'category')
        qs = self._apply_filters(qs, filters)
        total = qs.count()
        offset = (page - 1) * page_size
        product_models = list(qs[offset:offset + page_size])
        return self._hydrate_list(product_models, user_id), total

    def list_all(self, filters: dict, page: int, page_size: int) -> Tuple[List[Product], int]:
        qs = ProductModel.objects.filter(deleted_at__isnull=True).select_related('store', 'category')
        qs = self._apply_filters(qs, filters)
        total = qs.count()
        offset = (page - 1) * page_size
        product_models = list(qs[offset:offset + page_size])
        return self._hydrate_list(product_models, user_id=None), total

    def _apply_filters(self, qs, filters: dict):
        if filters.get('q'):
            qs = qs.filter(name__icontains=filters['q'])
        if filters.get('category_id'):
            qs = qs.filter(category_id=filters['category_id'])
        if filters.get('store_id'):
            qs = qs.filter(store_id=filters['store_id'])
        if filters.get('tag'):
            qs = qs.filter(product_tags__tag__slug=filters['tag'])
        if filters.get('status'):
            qs = qs.filter(status=filters['status'])
        if filters.get('min_price') is not None:
            qs = qs.filter(base_price__gte=filters['min_price'])
        if filters.get('max_price') is not None:
            qs = qs.filter(base_price__lte=filters['max_price'])
        if filters.get('rating_min') is not None:
            qs = qs.filter(rating_average__gte=filters['rating_min'])
        sort_map = {
            'newest': '-created_at',
            'price_asc': 'base_price',
            'price_desc': '-base_price',
            'rating': '-rating_average',
            'sold': '-sold_count',
        }
        qs = qs.order_by(sort_map.get(filters.get('sort', 'newest'), '-created_at'))
        return qs

    def _hydrate_list(self, product_models, user_id: Optional[str]) -> List[Product]:
        product_ids = [p.id for p in product_models]
        primary_images = {
            img.product_id: img.image_url
            for img in ProductImageModel.objects.filter(product_id__in=product_ids, is_primary=True, deleted_at__isnull=True)
        }
        fav_set = set()
        if user_id:
            fav_set = set(
                FavoriteModel.objects.filter(user_id=user_id, product_id__in=product_ids, deleted_at__isnull=True).values_list('product_id', flat=True)
            )
        products = []
        for p in product_models:
            domain_p = ProductPersistenceMapper.from_entity(p)
            if domain_p:
                domain_p.primary_image_url = primary_images.get(p.id)
                domain_p.is_favorite = (p.id in fav_set)
                products.append(domain_p)
        return products

    def get_by_id(self, product_id: str, user_id: Optional[str] = None) -> Optional[Product]:
        model = ProductModel.objects.filter(id=product_id, deleted_at__isnull=True).select_related('store', 'category').first()
        if not model:
            return None
        domain_p = ProductPersistenceMapper.from_entity(model)
        if not domain_p:
            return None

        imgs = self.get_images(product_id)
        domain_p.images = imgs
        primary = next((i for i in imgs if i.is_primary), None)
        domain_p.primary_image_url = primary.image_url if primary else (imgs[0].image_url if imgs else None)

        domain_p.variants = self.get_variants(product_id)

        domain_p.tags = [
            ProductPersistenceMapper.tag_from_entity(pt.tag)
            for pt in model.product_tags.select_related('tag').all()
        ]

        if user_id:
            domain_p.is_favorite = FavoriteModel.objects.filter(user_id=user_id, product_id=model.id, deleted_at__isnull=True).exists()

        return domain_p

    def get_by_store_and_slug(self, store_slug: str, product_slug: str, user_id: Optional[str] = None) -> Optional[Product]:
        model = ProductModel.objects.filter(
            store__slug=store_slug, slug=product_slug, status='active', deleted_at__isnull=True
        ).select_related('store', 'category').first()
        if not model:
            return None
        return self.get_by_id(str(model.id), user_id=user_id)

    def get_images(self, product_id: str) -> List[ProductImage]:
        imgs = ProductImageModel.objects.filter(product_id=product_id, deleted_at__isnull=True).order_by('sort_order')
        return [ProductPersistenceMapper.image_from_entity(i) for i in imgs if i is not None]

    def get_variants(self, product_id: str) -> List[ProductVariant]:
        variants = ProductVariantModel.objects.filter(product_id=product_id, status='active', deleted_at__isnull=True).prefetch_related('options')
        return [ProductPersistenceMapper.variant_from_entity(v) for v in variants if v is not None]

    def list_tags(self, page: int, page_size: int) -> Tuple[List[Tag], int]:
        qs = TagModel.objects.all()
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [ProductPersistenceMapper.tag_from_entity(t) for t in models if t is not None], total

    def exists_by_store_and_slug(self, store_id: str, slug: str, exclude_id: Optional[str] = None) -> bool:
        qs = ProductModel.objects.filter(store_id=store_id, slug=slug, deleted_at__isnull=True)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def save(self, product: Product, actor_id: Optional[str] = None) -> Product:
        db_instance = ProductModel.objects.filter(pk=product.id).first() if product.id else None
        is_new = db_instance is None
        db_instance = ProductPersistenceMapper.to_model(product, db_instance)
        if actor_id:
            if is_new:
                db_instance.created_by_id = actor_id
            db_instance.updated_by_id = actor_id
        db_instance.save()
        return ProductPersistenceMapper.from_entity(db_instance)

    def soft_delete(self, product_id: str, actor_id: Optional[str] = None) -> None:
        update_fields = {'deleted_at': timezone.now()}
        if actor_id:
            update_fields['deleted_by_id'] = actor_id
        ProductModel.objects.filter(pk=product_id, deleted_at__isnull=True).update(**update_fields)


    def is_favorite(self, product_id: str, user_id: str) -> bool:
        return FavoriteModel.objects.filter(user_id=user_id, product_id=product_id, deleted_at__isnull=True).exists()
