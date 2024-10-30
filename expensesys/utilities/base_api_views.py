from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny


class BaseAPIView(APIView):
    param_serializer = None
    query_param_serializer = None
    input_serializer = None
    output_serializer = None


class PublicAPIView(BaseAPIView):
    permission_classes = [
        AllowAny,
    ]


class AuthenticatedAPIView(BaseAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
