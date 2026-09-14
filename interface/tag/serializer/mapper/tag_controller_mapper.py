from typing import Dict, Any, List
from dataclasses import asdict
from domain.tag.entity.tag import Tag
from interface.tag.serializer.response.tag_response import TagResponse


class TagControllerMapper:

    @staticmethod
    def from_request(validated_data: Dict[str, Any]) -> Tag:
        return Tag(
            name=validated_data.get("name", ""),
            slug=validated_data.get("slug", ""),
        )

    @staticmethod
    def to_response(tag: Tag) -> Dict[str, Any]:
        response_dto = TagResponse(
            id=str(tag.id) if tag.id else None,
            name=tag.name,
            slug=tag.slug,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(tags: List[Tag]) -> List[Dict[str, Any]]:
        return [TagControllerMapper.to_response(t) for t in tags]
