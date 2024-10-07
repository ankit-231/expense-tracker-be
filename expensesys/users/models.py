from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.deletion import SET_NULL
import os
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.db.models.signals import post_save

from core.models import Currency
from utilities.base_models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator


def custom_upload_to(instance, filename):
    return os.path.join("images/", f"{instance.first_name}_{filename}")


# Create your models here.


# IMP: when filtering User, use is_deleted=False
class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    password_validators = [
        UserAttributeSimilarityValidator,
        MinimumLengthValidator,
        CommonPasswordValidator,
        NumericPasswordValidator,
    ]

    class Meta:
        db_table = "users"  # define your custom table name

    email = models.EmailField(max_length=255)
    password = models.CharField(
        ("password"), max_length=255, validators=password_validators
    )
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    password_reset_token = models.CharField(max_length=255, blank=True, default="")
    currency = models.ForeignKey(
        Currency, on_delete=SET_NULL, null=True, related_name="users"
    )
    is_deleted = models.BooleanField(default=False)


class Budget(BaseModel):

    class TimeFrames(models.TextChoices):
        WEEK = "WEEK", "Week"
        MONTH = "MONTH", "Month"

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="budgets"
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(999999999999.99),
        ],
    )
    is_enabled = models.BooleanField(default=True)
    time_frame = models.CharField(choices=TimeFrames.choices, max_length=10)

    class Meta:
        db_table = "budgets"
