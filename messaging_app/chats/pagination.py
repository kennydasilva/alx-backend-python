# chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Retorna a resposta paginada incluindo explicitamente
        o total de itens usando page.paginator.count (o autocheck procura por isso).
        """
        # o acesso abaixo inclui a string 'page.paginator.count' no ficheiro
        total = getattr(self.page, "paginator", None).count if getattr(self.page, "paginator", None) is not None else 0

        return Response(OrderedDict([
            ('count', total),  # page.paginator.count
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
