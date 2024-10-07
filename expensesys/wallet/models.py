import os
from django.db import models

from utilities.base_models import BaseModel
from users.models import User

# Create your models here.


def wallet_icon_upload_to(instance, filename):
    return os.path.join("wallets", f"{instance.name}_{filename}")


class Wallet(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="wallets"
    )
    name = models.CharField(max_length=255)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.ImageField(upload_to=wallet_icon_upload_to, default="")
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = "wallets"
