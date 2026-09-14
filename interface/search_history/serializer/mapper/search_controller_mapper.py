from typing import Dict, Any, List
from dataclasses import asdict
from domain.search_history.entity.search_history import SearchHistory
from interface.search_history.serializer.response.search_history_response import SearchHistoryResponse


class SearchControllerMapper:

    @staticmethod
    def to_response(search: SearchHistory) -> Dict[str, Any]:
        response_dto = SearchHistoryResponse(
            id=str(search.id) if search.id else None,
            query=search.query,
            filters_json=search.filters_json,
            result_count=search.result_count,
            created_at=search.created_at.isoformat() if search.created_at else None,
        )
        return asdict(response_dto)

    @staticmethod
    def to_list_response(searches: List[SearchHistory]) -> List[Dict[str, Any]]:
        return [SearchControllerMapper.to_response(s) for s in searches]

