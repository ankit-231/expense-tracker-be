from transaction.models import Transaction
from users.models import User
from wallet.models import Wallet


class UserUtil:
    def __init__(self, user: User) -> None:
        self.user = user

    def all_wallets(self, *args, **kwargs):
        wallets = Wallet.objects.filter(user=self.user, *args, **kwargs)
        return wallets

    def wallet_name_exists(self, name: str, exclude_name: str = None):
        from django.db import connection

        connection.queries.clear()

        name = name.lower().strip()

        # query = self.all_wallets(name=name)
        query = Wallet.objects.filter(user=self.user, name=name)

        if exclude_name:
            exclude_name = exclude_name.lower().strip()
            query = query.exclude(name=exclude_name)
        # Print all queries executed
        for qq in connection.queries:
            print(qq["sql"])

        return query.exists()

    def all_transactions(self, *args, **kwargs):
        transactions = Transaction.objects.filter(user=self.user, *args, **kwargs)
        return transactions
