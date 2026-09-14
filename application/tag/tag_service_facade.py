from typing import Dict, Any, Optional
from domain.tag.entity.tag import Tag
from domain.tag.exception.tag_exception import TagException
from domain.tag.ports.tag_repository import TagRepositoryInterface
from domain.tag.service.tag_service import TagServiceInterface
from interface.tag.serializer.mapper.tag_controller_mapper import TagControllerMapper


class TagServiceFacade(TagServiceInterface):

    def __init__(self, repo: TagRepositoryInterface):
        self.repo = repo

    def list(self, page: int, page_size: int) -> Dict[str, Any]:
        tags, total = self.repo.list(page, page_size)
        return {
            "items": TagControllerMapper.to_list_response(tags),
            "total": total,
        }

    def get(self, tag_id: str) -> Dict[str, Any]:
        tag = self.repo.get_by_id(tag_id)
        if not tag:
            raise TagException.not_found()
        return TagControllerMapper.to_response(tag)

    def create(self, data: dict, actor_id: Optional[str] = None) -> Dict[str, Any]:
        slug = data.get("slug", "")
        name = data.get("name", "")
        if self.repo.exists_by_slug(slug):
            raise TagException.already_exists(f"Tag with slug '{slug}' already exists")
        if self.repo.exists_by_name(name):
            raise TagException.already_exists(f"Tag with name '{name}' already exists")
        tag = TagControllerMapper.from_request(data)
        saved = self.repo.create(tag)
        return TagControllerMapper.to_response(saved)

    def update(self, tag_id: str, data: dict, partial: bool = False, actor_id: Optional[str] = None) -> Dict[str, Any]:
        existing = self.repo.get_by_id(tag_id)
        if not existing:
            raise TagException.not_found()

        new_slug = data.get("slug")
        if new_slug and new_slug != existing.slug:
            if self.repo.exists_by_slug(new_slug, exclude_id=existing.id):
                raise TagException.already_exists(f"Tag with slug '{new_slug}' already exists")
            existing.slug = new_slug

        new_name = data.get("name")
        if new_name and new_name != existing.name:
            if self.repo.exists_by_name(new_name, exclude_id=existing.id):
                raise TagException.already_exists(f"Tag with name '{new_name}' already exists")
            existing.name = new_name

        saved = self.repo.update(existing)
        return TagControllerMapper.to_response(saved)

    def delete(self, tag_id: str, actor_id: Optional[str] = None) -> None:
        existing = self.repo.get_by_id(tag_id)
        if not existing:
            raise TagException.not_found()
        self.repo.delete(tag_id)
