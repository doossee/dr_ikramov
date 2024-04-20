from django.contrib.auth import views

from rest_framework.response import Response
from rest_framework import pagination

from math import ceil


class CustomPagination(pagination.PageNumberPagination):
    """ """
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        limit = self.get_page_size(self.request)
        next_page = None
        previous_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()
        if self.page.has_previous():
            previous_page = self.page.previous_page_number()
        return Response({
            'next': self.get_next_link(),
            'next_page': next_page,
            'previous': self.get_previous_link(),
            'previous_page': previous_page,
            'count': self.page.paginator.count,
            'page_count': ceil(self.page.paginator.count / limit),
            'limit': limit,
            'results': data,
        })


class LogoutView(views.LogoutView):
    """ """
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
