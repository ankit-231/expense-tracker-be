class GetTransactionListPaginatedAPI(AuthenticatedAPIView):

    class OutputSerializer(serializers.Serializer):
        wallet_icon = serializers.SerializerMethodField()

        class TransactionSerializer(serializers.ModelSerializer):

            class Meta:
                model = Transaction
                fields = [
                    "id",
                    "wallet",
                    "wallet_icon",
                    "transaction_time",
                    "amount",
                    "description",
                ]

            def get_wallet_icon(self, obj):
                return obj.wallet.icon.data
            
        transaction_date = serializers.DateField()
        day = serializers.CharField()
        total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
        absolute_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
        transaction_type = serializers.CharField()
        transactions = TransactionSerializer(many=True)

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
        grouped_transactions = (
            Transaction.objects.values(
                "transaction_date",
            )
            .annotate(
                total_amount=Sum(
                    Case(
                        When(
                            transaction_type=Transaction.TransactionTypes.DEBIT,
                            then=F("amount") * -1,
                        ),
                        When(
                            transaction_type=Transaction.TransactionTypes.CREDIT,
                            then=F("amount"),
                        ),
                        output_field=DecimalField(),
                    )
                ),
                absolute_amount=Abs(
                    Sum(
                        Case(
                            When(
                                transaction_type=Transaction.TransactionTypes.DEBIT,
                                then=F("amount") * -1,
                            ),
                            When(
                                transaction_type=Transaction.TransactionTypes.CREDIT,
                                then=F("amount"),
                            ),
                            output_field=DecimalField(),
                        )
                    )
                ),
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
            .order_by("transaction_date")
        )
        user_ = UserUtil(request.user)
        for grouped_transaction in grouped_transactions:
            print(grouped_transaction)
            grouped_transaction["transactions"] = user_.all_transactions(
                transaction_date=grouped_transaction["transaction_date"]
            )
            grouped_transaction["day"] = get_week_day(grouped_transaction["day"])
        output_serializer = self.OutputSerializer(grouped_transactions, many=True)
        return OKResponse(data=output_serializer.data)
