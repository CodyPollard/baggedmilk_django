from django.contrib import admin
from .models import Timer, DucksInjury, DucksPlayer

# Register your models here.
admin.site.register(Timer)
admin.site.register(DucksInjury)
admin.site.register(DucksPlayer)