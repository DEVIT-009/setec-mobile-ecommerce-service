import uuid
from typing import List, Optional, Tuple

from domain.tag.entity.tag import Tag
from domain.tag.exception.tag_exception import TagException
from domain.tag.ports.tag_repository import TagRepositoryInterface
from infrastructure.persistence.models.product_model import Tag as TagModel


def _is_uuid(val: str) -> bool:
    try:
        uuid.UUID(str(val))
        return True
    except (ValueError, AttributeError, TypeError):
        return False


class TagRepositoryImpl(TagRepositoryInterface):

    def list(self, page: int, page_size: int) -> Tuple[List[Tag], int]:
        qs = TagModel.objects.all().order_by('name')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [self._to_domain(m) for m in models], total

    def get_by_id(self, tag_id: str) -> Optional[Tag]:
        if not _is_uuid(tag_id):
            return None
        model = TagModel.objects.filter(id=tag_id).first()
        return self._to_domain(model) if model else None

    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        qs = TagModel.objects.filter(slug=slug)
        if exclude_id and _is_uuid(exclude_id):
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def exists_by_name(self, name: str, exclude_id: Optional[str] = None) -> bool:
        qs = TagModel.objects.filter(name__iexact=name)
        if exclude_id and _is_uuid(exclude_id):
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def create(self, tag: Tag) -> Tag:
        model = TagModel(name=tag.name, slug=tag.slug)
        model.save()
        return self._to_domain(model)

    def update(self, tag: Tag) -> Tag:
        if not _is_uuid(str(tag.id)):
            raise TagException.not_found()
        model = TagModel.objects.filter(id=tag.id).first()
        if not model:
            raise TagException.not_found()
        model.name = tag.name
        model.slug = tag.slug
        model.save()
        return self._to_domain(model)

    def delete(self, tag_id: str) -> None:
        if not _is_uuid(tag_id):
            raise TagException.not_found()
        deleted, _ = TagModel.objects.filter(id=tag_id).delete()
        if not deleted:
            raise TagException.not_found()

    @staticmethod
    def _to_domain(model: TagModel) -> Tag:
        return Tag(
            id=str(model.id),
            name=model.name,
            slug=model.slug,
        )
