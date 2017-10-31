from datetime import timedelta, datetime
from django.shortcuts import render
from .forms import TimerForm
from .models import Timer
from baggedmilk_django.secret import TIMERBOARD_KEY
import re

# Create your views here.
def index(request):
    return render(request, 'milk/index.html')

def milkbot(request):
    return render(request, 'milk/milkbot.html')

def timerboard(request):
    # Create the form
    form = TimerForm(request.POST or None)
    # If the form has valid inputs, a model is created. If not an error is displayed for the user
    if form.is_valid():
        timer = form.save(commit=False)
        print('FORM HAS BEEN SUBMITTED')
        # Getting final timer
        try:
            t_days = int(re.findall('(\d+)', timer.end_at)[0])
            t_hours = int(re.findall('(\d+)', timer.end_at)[1])
            t_minutes = int(re.findall('(\d+)', timer.end_at)[2])
            timeleft = timedelta(days=t_days, hours=t_hours, minutes=t_minutes)
            timer.timer_ends_at = datetime.now()+timeleft
        except IndexError:
            pass
        timer.save()

    # Get all timers to display in template
    all_timers = Timer.objects.all()
    # Formats the timer to display to the user
    for timer in all_timers:
        # Delete expired timers
        if timer.timer_ends_at < datetime.now():
            timer.delete()
        # Ignores timers still in the future
        else:
            delta = timer.timer_ends_at - datetime.now()
            seconds = delta.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            timer.end_at = '%02d:%02d:%02d' % (hours, minutes, seconds)

    return render(request, 'milk/timerboard.html', {'form': form, 'all_timers': all_timers})
