from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings


class SimplePagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 25)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', 1)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data,
        })
