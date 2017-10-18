from datetime import datetime, timedelta
from django.db import models


# Create your models here.
class Testing(models.Model):
    test_string = models.CharField(max_length=50)


class Timer(models.Model):
    type = models.CharField(max_length=20)
    system = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.CharField(max_length=30)
    timer_ends_at = models.DateTimeField(default=datetime.now()+timedelta(hours=4))

    def __str__(self):
        return self.timer_ends_at
