# shared/pagination/paging.py
from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class Paging(Generic[T]):
    items: List[T]
    page: int
    size: int
    total: int
    total_pages: int

    @staticmethod
    def of(items, page, size, total, total_pages):
        return Paging(
            items=items,
            page=page,
            size=size,
            total=total,
            total_pages=total_pages
        )
