from utilities.general import get_colors_list
from utilities.model_utilities.users import UserUtil
from users.models import User
from utilities.exceptions import ApplicationError
from transaction.models import ChartTypes
from django.db.models import Sum, Case, When, F, DecimalField, Value, CharField
from transaction.models import (
    Category,
    ChartTypes,
    Transaction,
    TransactionWithEnabledWallet,
)
from django.db import models


class StatisticsUtil:
    def __init__(self, user: User, chart_type: str):
        self.user = user
        self.user_ = UserUtil(self.user)
        # self.chart_type = chart_type
        # self._check_chart_type()

    # def _check_chart_type(self):
    #     if self.chart_type not in ChartTypes.values:
    #         raise ApplicationError(f"Invalid chart type: {self.chart_type}")

    # def get_transactions(self, *args, **kwargs):
    #     pass

    def get_monthly_bargraph_data(self, year, month):
        # fetch transactions and aggregate data by day
        transactions = (
            self.user_.all_transactions(
                transaction_date__year=year, transaction_date__month=month
            )
            .values("transaction_date__day")
            .annotate(
                total_credit=Sum(
                    "amount",
                    filter=models.Q(
                        transaction_type=Transaction.TransactionTypes.CREDIT
                    ),
                ),
                total_debit=Sum(
                    "amount",
                    filter=models.Q(
                        transaction_type=Transaction.TransactionTypes.DEBIT
                    ),
                ),
            )
            .order_by("transaction_date__day")
        )

        # prepare the data for Chart.js
        labels = [f"Day {t['transaction_date__day']}" for t in transactions]
        total_credit_data = [
            (float(t["total_credit"]) if t["total_credit"] else 0) for t in transactions
        ]
        total_debit_data = [
            (float(t["total_debit"]) if t["total_debit"] else 0) for t in transactions
        ]

        output_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Total Credit",
                    "backgroundColor": "#42A5F5",
                    "borderColor": "#42A5F5",
                    "fill": False,
                    "data": total_credit_data,
                },
                {
                    "label": "Total Debit",
                    "backgroundColor": "#FFA726",
                    "borderColor": "#FFA726",
                    "fill": False,
                    "data": total_debit_data,
                },
            ],
        }

        return output_data

    def get_monthly_piechart_data(self, year, month, transaction_type: Transaction.TransactionTypes.values):
        # fetch transactions and aggregate data by category
        transactions = (
            self.user_.all_transactions(
                transaction_date__year=year,
                transaction_date__month=month,
                transaction_type=transaction_type,
            )
            .values("category", "category__name")
            .annotate(
                total_data=Sum(
                    "amount",
                    filter=models.Q(transaction_type=transaction_type),
                ),
            )
            .order_by("category")
        )

        # prepare the data for Chart.js
        labels = [f"{t['category__name']}" for t in transactions]
        total_data = [
            (float(t["total_data"]) if t["total_data"] else 0) for t in transactions
        ]

        print(transactions, "transactions")
        label = "Total " + Transaction.TransactionTypes(transaction_type).label
        output_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": label,
                    "backgroundColor": get_colors_list(len(transactions), "rgba"),
                    # "backgroundColor": ['hsl(0, 64%, 55%)', 'hsl(137, 64%, 55%)', 'hsl(274, 64%, 55%)'],
                    # "borderColor": get_colors_list(len(transactions)),
                    "borderColor": ['rgb(249, 115, 22)', 'rgb(6, 182, 212)', 'rgb(107, 114, 128)'],
                    "fill": False,
                    "data": total_data,
                },
            ],
        }

        return output_data
