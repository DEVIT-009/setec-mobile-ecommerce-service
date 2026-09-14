from shared.pagination.paging import Paging


class ApiPaging:
    """Converts a Paging object to the eCommerce API meta format."""

    @staticmethod
    def to_meta(paging: Paging, request_id=None) -> dict:
        page = paging.page
        page_size = paging.size
        total = paging.total
        has_next = (page * page_size) < total
        return {
            "page": page,
            "page_size": page_size,
            "total": total,
            "has_next": has_next,
            "request_id": request_id,
        }

    @staticmethod
    def from_request(request, default_size=20) -> dict:
        """Extract page and page_size from query params."""
        try:
            page = max(1, int(request.query_params.get("page", 1)))
        except (ValueError, TypeError):
            page = 1
        try:
            page_size = max(1, min(100, int(request.query_params.get("page_size", default_size))))
        except (ValueError, TypeError):
            page_size = default_size
        return {"page": page, "page_size": page_size}
