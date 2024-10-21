from django.shortcuts import render

# Create your views here.

from core.models import Icon
from utilities.base_api_views import AuthenticatedAPIView, PublicAPIView
from utilities.response_wrappers import OKResponse
from rest_framework import serializers


class GetIconListAPI(AuthenticatedAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Icon
            fields = ["id", "name", "class_name"]

    output_serializer = OutputSerializer

    def get(self, request):
        icons = Icon.objects.all()
        output_serializer = self.output_serializer(icons, many=True)
        return OKResponse(data=output_serializer.data)
