from django.shortcuts import render

from utilities.response_wrappers import OKResponse
from transaction.models import Transaction
from utilities.base_api_views import AuthenticatedAPIView, PublicAPIView
from rest_framework import serializers

# Create your views here.


class CreateTransactionAPI(AuthenticatedAPIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = [
                "user",
                "wallet",
                "transaction_date",
                "transaction_time",
                "transaction_type",
                "amount",
                "description",
                "category",
                "note",
                "image",
            ]
            extra_kwargs = {
                "user": {"required": True, "allow_null": False},
                "wallet": {"required": True, "allow_null": False},
                "category": {"required": True, "allow_null": False},
            }

    def post(self, request):
        data = request.data
        data.update({"user": request.user.id})
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return OKResponse(data=serializer.data)


class GetTransactionListAPI(PublicAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = [
                "wallet",
                "transaction_date",
                "transaction_time",
                "transaction_type",
                "amount",
                "description",
                "category",
                "note",
                "image",
            ]

    def get(self, request):
        query_params = request.query_params
        print(query_params)
        transactions = Transaction.objects.all()
        output_serializer = self.OutputSerializer(transactions, many=True)
        return OKResponse(data=output_serializer.data)
