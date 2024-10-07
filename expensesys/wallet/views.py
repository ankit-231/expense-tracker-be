from django.shortcuts import render

from wallet.models import Wallet
from utilities.response_wrappers import OKResponse
from utilities.base_api_views import PublicAPIView
from rest_framework import serializers

# Create your views here.


class CreateWalletAPI(PublicAPIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Wallet
            fields = [
                "name",
                "initial_amount",
                "icon",
            ]

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(message="Wallet created successfully")
