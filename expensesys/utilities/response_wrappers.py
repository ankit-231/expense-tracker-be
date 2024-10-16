# responses.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    PermissionDenied,
)
from django.http import Http404
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error


class OKResponse(Response):
    def __init__(self, *, message="Success", data=None, **kwargs):
        status_code = status.HTTP_200_OK
        response_data = {"data": data, "message": message, "status": status_code}
        super().__init__(data=response_data, status=status_code, **kwargs)


class BadResponse(Response):
    def __init__(
        self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST, **kwargs
    ):
        errors = errors or {}
        response_data = {"message": message, "extra": errors, "status": status_code}
        super().__init__(data=response_data, status=status_code, **kwargs)
