from django.shortcuts import render

from core.models import Icon
from utilities.exceptions import ApplicationError
from utilities.model_utilities.users import UserUtil
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
                # "is_enabled",
            ]
            extra_kwargs = {
                "user": {"required": True, "allow_null": False},
                # "icon": {"required": True, "allow_null": False},
                # "is_enabled": {"required": True},
            }

        def validate(self, data):
            user_ = UserUtil(self.context["request"].user)
            if user_.wallet_name_exists(data["name"]):
                raise serializers.ValidationError(
                    {"name": "Wallet name already exists"}
                )
            return data

    def post(self, request):
        data = request.data
        # default Icon
        icon = Icon.objects.first()
        data.update({"user": request.user.id, "icon": icon.id})
        input_serializer = self.InputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(
            message="Wallet created successfully", data=input_serializer.data
        )


class GetWalletDetailAPI(PublicAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        icon = serializers.SerializerMethodField()

        class Meta:
            model = Wallet
            fields = [
                "id",
                "name",
                "initial_amount",
                "icon",
                "is_enabled",
            ]

        def get_icon(self, obj):
            if obj.icon:
                return obj.icon.data
            return None

    def get(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            raise ApplicationError("Wallet not found")
        output_serializer = self.OutputSerializer(wallet)
        return OKResponse(data=output_serializer.data)


class GetWalletListAPI(PublicAPIView):

    class ParamSerializer(serializers.Serializer):
        result = serializers.ChoiceField(choices=["all", "enabled"])

    output_serializer = GetWalletDetailAPI.OutputSerializer

    def get(self, request, result):
        user = request.user
        param_serializer = self.ParamSerializer(data=self.kwargs)
        param_serializer.is_valid(raise_exception=True)

        enabled = param_serializer.data.get("result") == "enabled"

        user_ = UserUtil(user, enabled_wallet=enabled)

        wallets = user_.all_wallets()

        output_serializer = self.output_serializer(wallets, many=True)
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
            wallet = self.context["wallet"]
            user_ = UserUtil(self.context["request"].user)
            if user_.wallet_name_exists(data["name"], exclude_name=wallet.name):
                raise serializers.ValidationError(
                    {"name": "Wallet name already exists"}
                )
            return data

    def post(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            raise ApplicationError("Wallet not found")
        input_serializer = self.InputSerializer(
            wallet, data=request.data, context={"request": request, "wallet": wallet}
        )
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return OKResponse(
            data=input_serializer.data, message="Wallet updated successfully"
        )


class DeleteWalletAPI(PublicAPIView):

    output_serializer = GetWalletDetailAPI.OutputSerializer

    def delete(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            raise ApplicationError("Wallet not found")
        wallet.delete()
        serializer = self.output_serializer(instance=wallet)
        return OKResponse(data=serializer.data, message="Wallet deleted successfully")


class UpdateWalletStatusAPI(PublicAPIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Wallet
            fields = [
                "is_enabled",
            ]

    input_serializer = InputSerializer
    output_serializer = GetWalletDetailAPI.OutputSerializer

    def post(self, request, pk):
        user = request.user
        wallet = Wallet.objects.filter(user=user, pk=pk).last()
        if not wallet:
            raise ApplicationError("Wallet not found")
        input_serializer = self.input_serializer(wallet, data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        serializer = self.output_serializer(instance=wallet)
        return OKResponse(data=serializer.data, message="Wallet disabled successfully")
