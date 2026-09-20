import re
from typing import List, Optional, Tuple

from domain.tag.entity.tag import Tag
from domain.tag.exception.tag_exception import TagException
from domain.tag.ports.tag_repository import TagRepositoryInterface
from infrastructure.persistence.models.product_model import Tag as TagModel

_TAG_ID_PATTERN = re.compile(r'^tag-\d{6}$')


def _is_valid_tag_id(val: str) -> bool:
    return bool(_TAG_ID_PATTERN.match(val)) if val else False


class TagRepositoryImpl(TagRepositoryInterface):

    def list(self, page: int, page_size: int) -> Tuple[List[Tag], int]:
        qs = TagModel.objects.all().order_by('name')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [self._to_domain(m) for m in models], total

    def get_by_id(self, tag_id: str) -> Optional[Tag]:
        model = TagModel.objects.filter(id=tag_id).first()
        return self._to_domain(model) if model else None

    def exists_by_slug(self, slug: str, exclude_id: Optional[str] = None) -> bool:
        qs = TagModel.objects.filter(slug=slug)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def exists_by_name(self, name: str, exclude_id: Optional[str] = None) -> bool:
        qs = TagModel.objects.filter(name__iexact=name)
        if exclude_id:
            qs = qs.exclude(id=exclude_id)
        return qs.exists()

    def create(self, tag: Tag) -> Tag:
        model = TagModel(name=tag.name, slug=tag.slug)
        model.save()
        return self._to_domain(model)

    def update(self, tag: Tag) -> Tag:
        model = TagModel.objects.filter(id=tag.id).first()
        if not model:
            raise TagException.not_found()
        model.name = tag.name
        model.slug = tag.slug
        model.save()
        return self._to_domain(model)

    def delete(self, tag_id: str) -> None:
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
