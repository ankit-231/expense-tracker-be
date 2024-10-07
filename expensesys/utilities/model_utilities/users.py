from users.models import User
from wallet.models import Wallet


class UserUtil:
    def __init__(self, user: User) -> None:
        self.user = user

    def all_wallets(self, *args, **kwargs):
        wallets = Wallet.objects.filter(user=self.user, *args, **kwargs)
        return wallets

    def wallet_name_exists(self, name: str):
        name = name.lower().strip()
        return self.all_wallets(name=name).exists()
