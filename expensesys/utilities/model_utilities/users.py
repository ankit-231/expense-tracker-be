from transaction.models import Transaction, TransactionWithEnabledWallet
from users.models import User
from wallet.models import Wallet


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
