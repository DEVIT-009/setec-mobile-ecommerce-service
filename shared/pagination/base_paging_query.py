from django.core.paginator import Paginator
from shared.pagination.paging import Paging
from shared.pagination.page_number_util import PageNumberUtility

class BasePagingRepository:

    @staticmethod
    def paginate(queryset, query, keyword_field="title", category_field=None):
        if query.keyword:
            filter_kwargs = {f"{keyword_field}__icontains": query.keyword}
            queryset = queryset.filter(**filter_kwargs)

        if category_field and getattr(query, "category", None):
            filter_kwargs = {f"{category_field}": query.category}
            queryset = queryset.filter(**filter_kwargs)

        queryset = queryset.order_by('-id')

        paginator = Paginator(queryset, query.size_value)
        page_obj = paginator.get_page(PageNumberUtility.in_page(query.page_value) + 1)

        return Paging(
            items=list(page_obj.object_list),
            page=PageNumberUtility.out_page(page_obj.number - 1),
            size=page_obj.paginator.per_page,
            total=page_obj.paginator.count,
            total_pages=page_obj.paginator.num_pages
        )
