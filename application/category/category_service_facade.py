from typing import List, Dict, Any, Optional
from domain.category.ports.category_repository import CategoryRepositoryInterface
from domain.category.service.category_service import CategoryServiceInterface
from domain.category.entity.category import Category
from domain.category.exception.category_exception import CategoryException
from interface.category.serializer.mapper.category_controller_mapper import CategoryControllerMapper


class CategoryServiceFacade(CategoryServiceInterface):

    def __init__(self, repo: CategoryRepositoryInterface):
        self.repo = repo

    def list_active(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        categories = self.repo.list_active(parent_id)
        return CategoryControllerMapper.to_list_response(categories)

    def list_admin(self, parent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all non-deleted categories (active + inactive) for admin views."""
        categories = self.repo.list_admin(parent_id)
        return CategoryControllerMapper.to_list_response(categories)

    def get_tree(self) -> List[Dict[str, Any]]:
        roots = self.repo.get_root_categories()
        return [self._to_tree_dict(r) for r in roots]

    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        category = self.repo.get_by_slug(slug)
        if not category:
            raise CategoryException.not_found()
        return CategoryControllerMapper.to_response(category)

    def get_by_id(self, category_id: str) -> Dict[str, Any]:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise CategoryException.not_found()
        return CategoryControllerMapper.to_response(category)

    def _find_admin(self, identifier: str) -> Category:
        category = self.repo.get_by_id(identifier)
        if not category:
            category = self.repo.get_by_slug(identifier)
        if not category:
            raise CategoryException.not_found()
        return category

    def get_admin(self, identifier: str) -> Dict[str, Any]:
        """Fetch by id or slug regardless of status (non-deleted only)."""
        category = self._find_admin(identifier)
        return CategoryControllerMapper.to_response(category)

    # Alias for any older caller expecting get_by_slug_admin
    get_by_slug_admin = get_admin

    def _to_tree_dict(self, cat: Category) -> Dict[str, Any]:
        data = CategoryControllerMapper.to_response(cat)
        children = self.repo.get_children(cat.id)
        data['children'] = [self._to_tree_dict(c) for c in children]
        return data

    def create(self, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]:
        slug = data.get('slug')
        if not slug:
            raise CategoryException.already_exists("Category slug is required")
        if self.repo.exists_by_slug(slug):
            raise CategoryException.already_exists(f"Category with slug '{slug}' already exists")

        parent_id = data.get('parent_id')
        if parent_id:
            parent = self.repo.get_by_id(parent_id)
            if not parent:
                raise CategoryException.invalid_parent("Parent category does not exist")

        category = CategoryControllerMapper.from_request(data)
        saved = self.repo.create(category, actor_id=actor_id)
        return CategoryControllerMapper.to_response(saved)

    def update(self, category_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        existing = self.repo.get_by_id(category_id)
        if not existing:
            raise CategoryException.not_found()

        new_slug = data.get('slug')
        if new_slug and new_slug != existing.slug:
            if self.repo.exists_by_slug(new_slug, exclude_id=existing.id):
                raise CategoryException.already_exists(f"Category with slug '{new_slug}' already exists")
            existing.slug = new_slug

        if 'name' in data or not partial:
            if 'name' in data:
                existing.name = data['name']
        if 'parent_id' in data:
            parent_id = data.get('parent_id')
            if parent_id:
                if str(parent_id) == str(existing.id):
                    raise CategoryException.invalid_parent("Category cannot be its own parent")
                parent = self.repo.get_by_id(parent_id)
                if not parent:
                    raise CategoryException.invalid_parent("Parent category does not exist")
            existing.parent_id = parent_id
        if 'icon_url' in data or not partial:
            if 'icon_url' in data:
                existing.icon_url = data['icon_url']
        if 'image_url' in data or not partial:
            if 'image_url' in data:
                existing.image_url = data['image_url']
        if 'sort_order' in data or not partial:
            if 'sort_order' in data:
                existing.sort_order = data['sort_order']
        if 'status' in data or not partial:
            if 'status' in data:
                existing.status = data['status']

        saved = self.repo.update(existing, actor_id=actor_id)
        return CategoryControllerMapper.to_response(saved)

    def soft_delete(self, category_id: str, actor_id: Optional[str] = None) -> None:
        existing = self.repo.get_by_id(category_id)
        if not existing:
            raise CategoryException.not_found()
        self.repo.soft_delete(existing.id, actor_id=actor_id)

