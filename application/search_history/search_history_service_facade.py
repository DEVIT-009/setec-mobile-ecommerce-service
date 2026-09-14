from typing import Dict, Any
from domain.search_history.ports.search_repository import SearchRepositoryInterface
from domain.search_history.service.search_service import SearchServiceInterface
from domain.search_history.entity.search_history import SearchHistory
from interface.search_history.serializer.mapper.search_controller_mapper import SearchControllerMapper


class SearchHistoryServiceFacade(SearchServiceInterface):

    def __init__(self, repo: SearchRepositoryInterface):
        self.repo = repo

    def record(self, user_id: str, data: dict) -> Dict[str, Any]:
        record = SearchHistory(
            user_id=user_id,
            query=data['query'],
            filters_json=data.get('filters_json'),
            result_count=data.get('result_count'),
        )
        saved = self.repo.save(record)
        return SearchControllerMapper.to_response(saved)

    def list(self, user_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        records, total = self.repo.list_by_user(user_id, page, page_size)
        return {
            "items": SearchControllerMapper.to_list_response(records),
            "total": total,
        }

    def delete(self, user_id: str, search_id: str) -> None:
        self.repo.delete_by_id(search_id, user_id)

    def clear(self, user_id: str) -> None:
        self.repo.clear_all(user_id)
