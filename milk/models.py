from datetime import datetime, timedelta
from django.db import models


# Create your models here.
class Testing(models.Model):
    test_string = models.CharField(max_length=50)


class Timer(models.Model):
    # Types
    TYPE_CHOICES = ['EC - Sotiyo', 'EC - Azbel', 'EC - Raitaru', 'Cit - Keepstar', 'Cit - Fortizar',
                    'Cit - Astrahus']
    type = models.CharField(max_length=20, choices=((x, x) for x in TYPE_CHOICES))
    system = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.CharField(max_length=30)
    timer_ends_at = models.DateTimeField(default=datetime.now()+timedelta(hours=4))

    def __str__(self):
        return str(self.timer_ends_at)


class DucksInjury(models.Model):
    # Model Fields
    published = models.BooleanField(default=False)
    last_injury = models.DateTimeField(default=datetime.now())
    news_link = models.CharField(default='', max_length=150)
    news_updates = models.TextField(default='There are no updates at this time.')
    description = models.TextField(blank=True)
    headline = models.CharField(default=str(last_injury), max_length=150)

    def __str__(self):
        return self.headline
