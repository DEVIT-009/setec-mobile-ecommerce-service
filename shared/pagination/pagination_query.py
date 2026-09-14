from dataclasses import dataclass
from typing import Optional


@dataclass
class PaginationQuery:
    page: Optional[int] = None
    size: Optional[int] = None
    keyword: Optional[str] = None
    category: Optional[int] = None
    sort_by: Optional[str] = None

    @property
    def page_value(self) -> int:
        return self.page if self.page is not None else 1

    @property
    def size_value(self) -> int:
        return self.size if self.size is not None else 10
