from django.contrib import admin
from .models import Timer, DucksInjury, DucksPlayer, PollQuestion, PollChoice

# Register your models here.
admin.site.register(Timer)
admin.site.register(DucksInjury)
admin.site.register(DucksPlayer)
admin.site.register(PollQuestion)
admin.site.register(PollChoice)