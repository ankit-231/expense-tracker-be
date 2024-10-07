from django.db import models

from users.models import User
from utilities.base_models import BaseModel

# Create your models here.


class Budget(BaseModel):

    class TimeFrames(models.TextChoices):
        WEEK = "WEEK", "Week"
        MONTH = "MONTH", "Month"

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="budgets"
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_enabled = models.BooleanField(default=True)
    time_frame = models.CharField(choices=TimeFrames.choices, max_length=10)

    class Meta:
        db_table = "budgets"
