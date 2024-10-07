# responses.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error

from .exceptions import ApplicationError


def custom_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }

    # note: Taken from https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#errors--exception-handling

    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:

        # our custom error
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra,
                "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {"fields": response.data["detail"]}
        response.data["status"] = status.HTTP_400_BAD_REQUEST

    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}
        response.data["status"] = status.HTTP_400_BAD_REQUEST

    del response.data["detail"]

    return response
