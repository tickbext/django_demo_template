from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CalcHistory(models.Model):
    date = models.DateTimeField()
    first = models.IntegerField()
    second = models.IntegerField()
    result = models.IntegerField()
    author = models.ForeignKey(to=User, default=1, on_delete=models.CASCADE)
