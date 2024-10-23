from django.forms import FloatField
from django.shortcuts import render

from utilities.statistics import StatisticsUtil
from utilities.general import get_week_day
from utilities.model_utilities.users import UserUtil
from utilities.exceptions import ApplicationError
from utilities.response_wrappers import OKResponse
from transaction.models import (
    Category,
    ChartTypes,
    Transaction,
    TransactionWithEnabledWallet,
)
from utilities.base_api_views import AuthenticatedAPIView, PublicAPIView
from rest_framework import serializers
from django.db.models.functions import ExtractWeekDay, Abs
from django.db.models import Sum, Case, When, F, DecimalField, Value, CharField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

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

        def validate(self, data):
            category = data.get("category")
            transaction_type = data.get("transaction_type")
            if category.category_type != transaction_type:
                raise serializers.ValidationError(
                    {"category": ["Transaction type and category type do not match"]}
                )
            return data

    def post(self, request):
        data = request.data
        data.update({"user": request.user.id})
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return OKResponse(data=serializer.data)


class GetTransactionDetailAPI(PublicAPIView):
    wallet_icon = serializers.SerializerMethodField()

    class OutputSerializer(serializers.ModelSerializer):
        wallet_icon = serializers.SerializerMethodField()

        class Meta:
            model = Transaction
            fields = [
                "id",
                "wallet",
                "transaction_date",
                "transaction_time",
                "transaction_type",
                "amount",
                "description",
                "category",
                "note",
                "image",
                "wallet_icon",
            ]

        def get_wallet_icon(self, obj):
            return obj.wallet.icon.data

    def get(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)

        output_serializer = self.OutputSerializer(transaction)
        return OKResponse(data=output_serializer.data)


class GetTransactionListAPI(PublicAPIView):

    output_serializer = GetTransactionDetailAPI.OutputSerializer

    def get(self, request):
        query_params = request.query_params
        print(query_params)
        transactions = Transaction.objects.all()
        output_serializer = self.output_serializer(transactions, many=True)
        return OKResponse(data=output_serializer.data)


class DeleteTransactionAPI(PublicAPIView):

    output_serializer = GetTransactionDetailAPI.OutputSerializer

    def delete(self, request, pk):
        transaction = Transaction.objects.filter(pk=pk).last()
        if not transaction:
            raise ApplicationError("Transaction not found")
        transaction.delete()
        serializer = self.output_serializer(instance=transaction)
        return OKResponse(data=serializer.data)


class GetTransactionListPaginatedAPI(AuthenticatedAPIView):

    class OutputSerializer(serializers.Serializer):

        transaction_date = serializers.DateField()
        day = serializers.CharField()
        total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
        absolute_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
        transaction_type = serializers.CharField()
        transactions = GetTransactionDetailAPI.OutputSerializer(many=True)

    def get(self, request):
        query_params = request.query_params
        print(query_params)
        """
        grouped_transactions = (
            Transaction.objects.values(
                "transaction_date",
            )
            .annotate(
                total_amount=Sum("amount"),
                day=ExtractWeekDay("transaction_date"),
            )
            .order_by("transaction_date")
        )

        total_amount should be the sum of amount but amount is negative if transaction_type == db and + if cr
        """
        print("hehe")
        user_ = UserUtil(request.user)

        total_amount_q = Sum(
            Case(
                When(
                    transaction_type=Transaction.TransactionTypes.DEBIT,
                    then=F("amount") * -1,
                ),
                When(
                    transaction_type=Transaction.TransactionTypes.CREDIT,
                    then=F("amount"),
                ),
                default=0,
                output_field=DecimalField(),
            )
        )
        grouped_transactions = (
            user_.all_transactions()
            .values(
                "transaction_date",
            )
            .annotate(
                total_amount=total_amount_q,
                absolute_amount=Abs(total_amount_q),
                transaction_type=Case(  # "+" or "-" based on transaction_type
                    When(
                        total_amount__lt=0,
                        then=Value(Transaction.TransactionTypes.DEBIT),
                    ),
                    When(
                        total_amount__gte=0,
                        then=Value(Transaction.TransactionTypes.CREDIT),
                    ),
                    output_field=CharField(),
                ),
                day=ExtractWeekDay("transaction_date"),
            )
            .order_by("-transaction_date")
        )
        for grouped_transaction in grouped_transactions:
            print(grouped_transaction)
            grouped_transaction["transactions"] = user_.all_transactions(
                transaction_date=grouped_transaction["transaction_date"]
            )
            grouped_transaction["day"] = get_week_day(grouped_transaction["day"])
        output_serializer = self.OutputSerializer(grouped_transactions, many=True)
        return OKResponse(data=output_serializer.data)


class UpdateTransactionAPI(AuthenticatedAPIView):
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
                "image": {"required": True, "allow_null": True},
            }

    input_serializer = InputSerializer

    def post(self, request, pk):
        data = request.data
        data.update({"user": request.user.id})
        transaction = Transaction.objects.filter(pk=pk, user=request.user).last()
        if not transaction:
            raise ApplicationError("Transaction not found")

        input_serializer = self.input_serializer(transaction, data=data)

        input_serializer.is_valid(raise_exception=True)

        input_serializer.save()

        return OKResponse(data=input_serializer.data)


class GetTransactionCategoryListAPI(PublicAPIView):

    class ParamSerializer(serializers.Serializer):
        category_type = serializers.ChoiceField(choices=Category.CategoryTypes.choices)

    class OutputSerializer(serializers.ModelSerializer):
        icon = serializers.SerializerMethodField()

        class Meta:
            model = Category
            fields = [
                "id",
                "name",
                "category_type",
                "icon",
            ]

        def get_icon(self, obj):
            return obj.icon.class_name

    def get(self, request, category_type):
        param_serializer = self.ParamSerializer(data=self.kwargs)
        param_serializer.is_valid(raise_exception=True)
        categories = Category.objects.filter(category_type=category_type)
        output_serializer = self.OutputSerializer(categories, many=True)
        return OKResponse(data=output_serializer.data)


# class GetMonthlyStatisticsAPI(PublicAPIView):

#     class ParamSerializer(serializers.Serializer):
#         pass

#     class OutputSerializer(serializers.Serializer):
#         pass

#     def get(self, request, year, month):
#         param_serializer = self.ParamSerializer(data=self.kwargs)
#         param_serializer.is_valid(raise_exception=True)
#         output_serializer = self.OutputSerializer()
#         return OKResponse(data=output_serializer.data)


class GetMonthlyStatisticsAPI(AuthenticatedAPIView):

    class QueryParamSerializer(serializers.Serializer):
        chart_type = serializers.ChoiceField(choices=ChartTypes.choices)

    class ParamSerializer(serializers.Serializer):
        year = serializers.IntegerField(required=True, min_value=1)
        month = serializers.IntegerField(required=True, min_value=1, max_value=12)

    class OutputSerializer(serializers.Serializer):

        # class DatasetSerializer(serializers.Serializer):
        #     label = serializers.CharField()
        #     backgroundColor = serializers.CharField()
        #     borderColor = serializers.CharField()
        #     fill = serializers.BooleanField()
        #     data = serializers.ListField()

        labels = serializers.ListField(child=serializers.CharField())
        datasets = serializers.ListField()

    def get(self, request, year, month):
        query_param_serializer = self.QueryParamSerializer(data=request.query_params)
        query_param_serializer.is_valid(raise_exception=True)

        param_serializer = self.ParamSerializer(data={"year": year, "month": month})
        param_serializer.is_valid(raise_exception=True)

        chart_type = query_param_serializer.data.get("chart_type")

        statistics_ = StatisticsUtil(request.user, chart_type)

        output_data = {}

        if chart_type == ChartTypes.BAR_GRAPH:
            output_data = statistics_.get_monthly_bargraph_data(year, month)
        elif chart_type == ChartTypes.PIE_CHART_CREDIT:
            output_data = statistics_.get_monthly_piechart_data(
                year, month, Transaction.TransactionTypes.CREDIT
            )
        elif chart_type == ChartTypes.PIE_CHART_DEBIT:
            output_data = statistics_.get_monthly_piechart_data(
                year, month, Transaction.TransactionTypes.DEBIT
            )

        output_serializer = self.OutputSerializer(output_data)
        return OKResponse(data=output_serializer.data)
