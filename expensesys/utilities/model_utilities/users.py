from transaction.models import Transaction, TransactionWithEnabledWallet
from users.models import User
from wallet.models import Wallet
from django.db.models import Sum
from django.db import models


class UserUtil:
    def __init__(self, user: User, enabled_wallet=True) -> None:
        self.user = user
        self.enabled_wallet = enabled_wallet

    def all_wallets(self, *args, **kwargs):
        kwargs.update({"user": self.user})
        if self.enabled_wallet:
            kwargs.update({"is_enabled": True})
        wallets = Wallet.objects.filter(*args, **kwargs)
        return wallets

    def wallet_name_exists(self, name: str, exclude_name: str = None):
        from django.db import connection

        connection.queries.clear()

        name = name.lower().strip()

        query = self.all_wallets(name=name)

        if exclude_name:
            exclude_name = exclude_name.lower().strip()
            query = query.exclude(name=exclude_name)
        # Print all queries executed
        for qq in connection.queries:
            print(qq["sql"])

        return query.exists()

    def all_transactions(self, *args, **kwargs):
        if self.enabled_wallet:
            transactions = TransactionWithEnabledWallet.objects.filter(
                user=self.user, *args, **kwargs
            )
        else:
            transactions = Transaction.objects.filter(user=self.user, *args, **kwargs)
        return transactions

    def get_remaining_balance(self):
        total_wallet_initial_balance = self.all_wallets().aggregate(
            total_initial_balance=Sum("initial_amount")
        )["total_initial_balance"]
        print(total_wallet_initial_balance)
        # transactions = self.all_transactions()
        totals = self.all_transactions().aggregate(
            total_credit=Sum(
                "amount",
                filter=models.Q(transaction_type=Transaction.TransactionTypes.CREDIT),
                default=0,
            ),
            total_debit=Sum(
                "amount",
                filter=models.Q(transaction_type=Transaction.TransactionTypes.DEBIT),
                default=0,
            ),
        )

        total_credit = totals["total_credit"]
        total_debit = totals["total_debit"]
        remaining_balance = total_wallet_initial_balance - total_debit + total_credit
        return remaining_balance
