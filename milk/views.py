from datetime import timedelta, datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .forms import TimerForm
from .models import Timer
import re

# Create your views here.
def index(request):
    return render(request, 'milk/index.html')

def milkbot(request):
    return render(request, 'milk/milkbot.html')

def timerboard(request):
    form = TimerForm(request.POST or None)
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

    all_timers = Timer.objects.all()
    for timer in all_timers:
        delta = timer.timer_ends_at - datetime.now()
        seconds = delta.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        timer.end_at = '{}:{}:{}'.format(int(hours), int(minutes), int(seconds))



    return render(request, 'milk/timerboard.html', {'form': form, 'all_timers': all_timers})
