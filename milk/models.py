from datetime import datetime, timedelta
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import random, string


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


class DucksPlayer(models.Model):
    name = models.CharField(max_length=100, default='Undefined')
    position = models.CharField(max_length=15, default='None')
    salary = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    healthy = models.BooleanField(default=False)
    injury_type = models.CharField(max_length=50, default='N/A')

    def __str__(self):
        return self.name


class IndividualPlayer(models.Model):
    name = models.CharField(max_length=100, default='Undefined')
    pos = models.CharField(max_length=15, default='None')
    salary = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    healthy = models.BooleanField(default=False)
    injury_type = models.CharField(max_length=50, default='N/A')
    games_missed = models.TextField(null=True)
    games_played = models.TextField(null=True)
    injury_streaks = models.TextField(null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class DucksInjury(models.Model):
    # Model Fields
    id = models.AutoField(primary_key=True)
    published = models.BooleanField(default=False)
    player = models.ForeignKey(DucksPlayer, default=1, on_delete=models.CASCADE)
    last_injury = models.DateTimeField(default=datetime.now)
    news_link = models.CharField(default='', max_length=150)
    news_updates = models.TextField(default='There are no updates at this time.')
    description = models.TextField(blank=True)
    headline = models.CharField(default=str(last_injury), max_length=150)

    def __str__(self):
        return self.headline


class PollQuestion(models.Model):
    id = models.CharField(primary_key=True, default=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4)), max_length=4)
    question = models.TextField(blank=True)

    def __str__(self):
        return '{} : {}'.format(self.question, self.id)


class PollChoice(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE, null=True)
    choice_text = models.CharField(max_length=250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
