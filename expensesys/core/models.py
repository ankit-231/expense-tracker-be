from django.db import models

from utilities.base_models import BaseModel

# Create your models here.


class Currency(BaseModel):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    class Meta:
        db_table = "currencies"


class ServerSetupLog(models.Model):
    setup_name = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.setup_name

    class Meta:
        db_table = "server_setup_logs"


class Icon(models.Model):
    name = models.CharField(max_length=255)
    svg_data = models.TextField()  # raw svg code may remove in the future
    class_name = models.CharField(max_length=255, default="")

    @property
    def data(self):
        return self.class_name or self.svg_data

    def __str__(self):
        return self.name

    class Meta:
        db_table = "icons"
