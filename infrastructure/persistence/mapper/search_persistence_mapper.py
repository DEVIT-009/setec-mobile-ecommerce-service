from typing import Optional
from domain.search_history.entity.search_history import SearchHistory as DomainSearchHistory
from infrastructure.persistence.models.search_model import SearchHistory as SearchHistoryModel


class SearchPersistenceMapper:

    @staticmethod
    def from_entity(entity: Optional[SearchHistoryModel]) -> Optional[DomainSearchHistory]:
        if entity is None:
            return None
        return DomainSearchHistory(
            id=str(entity.id),
            user_id=str(entity.user_id) if entity.user_id else None,
            query=entity.query,
            filters_json=entity.filters_json,
            result_count=entity.result_count,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_model(domain: DomainSearchHistory, model_instance: Optional[SearchHistoryModel] = None) -> SearchHistoryModel:
        model = model_instance or SearchHistoryModel()
        if domain.user_id:
            model.user_id = domain.user_id
        model.query = domain.query
        model.filters_json = domain.filters_json
        model.result_count = domain.result_count
        return model
