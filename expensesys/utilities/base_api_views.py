from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated, AllowAny


class BaseAPIView(APIView):
    pass


class PublicAPIView(BaseAPIView):
    permission_classes = [
        AllowAny,
    ]


class AuthenticatedAPIView(BaseAPIView):
    permission_classes = [
        IsAuthenticated,
    ]
