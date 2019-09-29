from django.contrib import admin
from .models import Timer, DucksInjury, PollQuestion, PollChoice, IndividualPlayer, IndividualGame, RegularSeasonGame

# Register your models here.
admin.site.register(Timer)
admin.site.register(DucksInjury)
admin.site.register(IndividualPlayer)
admin.site.register(IndividualGame)
admin.site.register(RegularSeasonGame)
admin.site.register(PollQuestion)
admin.site.register(PollChoice)
