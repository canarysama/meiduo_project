from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Meiduopagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'pagesize'

    # 重写分页
    def get_paginated_response(self, data):
        return Response(
            {

                "counts": self.page.paginator.count,

                "lists": data,

                "page": self.page.number,

                "pages": self.page.paginator.num_pages,

                "pagesize": self.page_size,
            }

        )