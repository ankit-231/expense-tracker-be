from django.shortcuts import render

from expensesys.utilities.exceptions import ApplicationError
from expensesys.utilities.model_utilities.users import UserUtil
from wallet.models import Wallet
from utilities.response_wrappers import BadResponse, OKResponse
from utilities.base_api_views import PublicAPIView
from rest_framework import serializers

# Create your views here.


class CreateWalletAPI(PublicAPIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Wallet
            fields = [
                "user",
                "name",
                "initial_amount",
                "icon",
                "is_enabled",
            ]

        def validate(self, data):
            user_ = UserUtil(self.context["request"].user)
            if user_.wallet_name_exists(data["name"]):
                raise serializers.ValidationError(
                    {"name": "Wallet name already exists"}
                )
            return data

    def post(self, request):
        data = request.data
        data.update({"user": request.user.id})
        input_serializer = self.InputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(message="Wallet created successfully")


class GetWalletDetailAPI(PublicAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Wallet
            fields = [
                "name",
                "initial_amount",
                "icon",
                "is_enabled",
            ]

    def get(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            return ApplicationError("Wallet not found")
        output_serializer = self.OutputSerializer(wallet)
        return OKResponse(data=output_serializer.data)


class GetWalletListAPI(PublicAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Wallet
            fields = [
                "name",
                "initial_amount",
                "icon",
                "is_enabled",
            ]

    def get(self, request):
        user = request.user
        wallets = Wallet.objects.filter(user=user)
        output_serializer = self.OutputSerializer(wallets, many=True)
        return OKResponse(data=output_serializer.data)


class UpdateWalletAPI(PublicAPIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Wallet
            fields = [
                "name",
                "initial_amount",
                "icon",
                "is_enabled",
            ]

        def validate(self, data):
            user_ = UserUtil(self.context["request"].user)
            if user_.wallet_name_exists(data["name"]):
                raise serializers.ValidationError(
                    {"name": "Wallet name already exists"}
                )
            return data

    def post(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            return ApplicationError("Wallet not found")
        input_serializer = self.InputSerializer(
            wallet, data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(message="Wallet updated successfully")


class DeleteWalletAPI(PublicAPIView):
    def post(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            return ApplicationError("Wallet not found")
        wallet.delete()
        return OKResponse(message="Wallet deleted successfully")
