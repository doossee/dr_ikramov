from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ErrorMiddleware:
    """ """

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
            response = Response({"message": exception.message}, status=status.HTTP_400_BAD_REQUEST)

        elif isinstance(exception, IntegrityError):
            response = Response(
                {"message": exception.__str__().split('\n')[1].strip("DETAIL: ")},
                status=status.HTTP_400_BAD_REQUEST
            )

        else:
            response = Response({"message": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()
        return response
