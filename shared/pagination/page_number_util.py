class PageNumberUtility:

    @staticmethod
    def in_page(page: int) -> int:
        return page - 1

    @staticmethod
    def out_page(page: int) -> int:
        return page + 1