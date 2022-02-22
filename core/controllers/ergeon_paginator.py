from django.core.paginator import Paginator
from django.db.models import QuerySet
from core.decorators import log_last_query


class ErgeonPaginator(Paginator):
    """
        Facilitator class to help the pagination manipulation
    """

    def __init__(self, size: int, page: int, query_set: QuerySet):
        super().__init__(query_set, size)
        self._actual_page = self.page(page)

    @log_last_query()
    def get_response(self) -> (dict, list):

        data = {
            "count": self.count,
            "num_pages": self.num_pages,
            "next_page_number": None
        }

        if self._actual_page.has_other_pages():
            data["next_page_number"] = self._actual_page.next_page_number()

        return data, self._actual_page.object_list
