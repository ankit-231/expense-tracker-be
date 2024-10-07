from django.db import models

from core.models import Icon
from utilities.base_models import BaseModel

from users.models import User
from wallet.models import Wallet
from django.utils import timezone

# Create your models here.


class Category(BaseModel):

    class CategoryTypes(models.TextChoices):
        CREDIT = "cr"
        DEBIT = "db"

    name = models.CharField(max_length=100)
    category_type = models.CharField(choices=CategoryTypes.choices, max_length=10)
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Transaction(BaseModel):

    class TransactionTypes(models.TextChoices):
        CREDIT = "cr"
        DEBIT = "db"

    def transaction_upload_to(self, filename):
        today = timezone.now()
        return f"transactions/{self.user_id}/{self.user.username}/{today.strftime('%Y-%m-%d_%H-%M-%S-%f')}.jpg"

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    transaction_date = models.DateField()
    transaction_time = models.TimeField()
    transaction_type = models.CharField(choices=TransactionTypes.choices, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    note = models.TextField()
    image = models.ImageField(upload_to=transaction_upload_to, null=True, blank=True)

    class Meta:
        db_table = "transactions"
