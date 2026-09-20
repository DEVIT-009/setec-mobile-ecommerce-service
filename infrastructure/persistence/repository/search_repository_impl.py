from typing import Optional, List, Tuple
from domain.search_history.ports.search_repository import SearchRepositoryInterface
from domain.search_history.entity.search_history import SearchHistory
from infrastructure.persistence.mapper.search_persistence_mapper import SearchPersistenceMapper
from infrastructure.persistence.models.search_model import SearchHistory as SearchHistoryModel


class SearchRepositoryInterfaceImpl(SearchRepositoryInterface):

    def upsert_by_query(self, record: SearchHistory) -> SearchHistory:
        """
        Find an existing record for (user_id, query).
        - Exists  → update filters_json and result_count, then save.
        - Missing → create a new record.
        Django's update_or_create handles both atomically.
        """
        defaults = {
            'filters_json': record.filters_json,
            'result_count': record.result_count,
        }
        db_instance, _ = SearchHistoryModel.objects.update_or_create(
            user_id=record.user_id,
            query=record.query,
            defaults=defaults,
        )
        return SearchPersistenceMapper.from_entity(db_instance)

    def list_by_user(self, user_id: str, page: int, page_size: int) -> Tuple[List[SearchHistory], int]:
        qs = SearchHistoryModel.objects.filter(user_id=user_id).order_by('-created_at')
        total = qs.count()
        offset = (page - 1) * page_size
        models = list(qs[offset:offset + page_size])
        return [SearchPersistenceMapper.from_entity(m) for m in models if m is not None], total

    def delete_by_id(self, search_id: str, user_id: str) -> bool:
        deleted_count, _ = SearchHistoryModel.objects.filter(id=search_id, user_id=user_id).delete()
        return deleted_count > 0

    def clear_all(self, user_id: str) -> None:
        SearchHistoryModel.objects.filter(user_id=user_id).delete()
