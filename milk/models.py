from django.db import models

# Create your models here.
class Testing(models.Model):

    test_string = models.CharField(max_length=50)
