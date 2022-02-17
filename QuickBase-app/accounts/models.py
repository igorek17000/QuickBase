from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class APIKey(models.Model):
    FTX = 'FTX'
    BINANCE = 'BIN'
    Exchange_platforme = [
        (FTX, 'FTX'),
        (BINANCE, 'Binance'),
    ]
    exchange = models.CharField(
        max_length=3,
        choices=Exchange_platforme,
        default=FTX,
    )
    apiKey = models.CharField(max_length=50)
    apiKeySecret = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)