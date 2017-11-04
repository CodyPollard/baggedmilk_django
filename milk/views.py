from datetime import timedelta, datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import TimerForm, PasteComparisonForm, InjuryUpdateForm
from .models import Timer, DucksInjury
from django.core.mail import send_mail
import re


# Create your views here.
def index(request):
    return render(request, 'milk/index.html')


def milkbot(request):
    return render(request, 'milk/milkbot.html')

def wwdli_success(request):
    injury_obj = DucksInjury.objects.first()
    return render(request, 'milk/wwdli-success.html', {'injury_obj': injury_obj})

def wwdli(request):
    injury_obj = DucksInjury.objects.first()
    # Form
    form = InjuryUpdateForm(request.POST or None)
    if form.is_valid():
        news_link = form.cleaned_data['news_link']
        description = form.cleaned_data['description']
        email_body = 'News Link: {}\nDescription: {}'.format(news_link, description)
        send_mail('Injury Update', email_body, 'baggedmilkme@gmail.com', ['codypollardeve@gmail.com'], fail_silently=False)
        return redirect('wwdli-success')

    return render(request, 'milk/wwdli.html', {'injury_obj': injury_obj, 'form': form})


def paste_results(request):
    return render(request, 'milk/paste-results.html')


def pastecomparison(request):
    # Create form
    form = PasteComparisonForm(request.POST or None)
    # Check for valid form
    if form.is_valid():
        results = []
        # Clean form data
        paste_one = form.cleaned_data['paste_one'].splitlines()
        paste_two = form.cleaned_data['paste_two'].splitlines()
        # Loop through paste_one and check against all of paste_two
        for i in paste_one:
            for j in paste_two:
                if i == j:
                    results.append(i)
        # Render a results page and pass it the list of results
        return render(request, 'milk/paste-results.html', {'results': results})

    return render(request, 'milk/pastecomparison.html', {'form': form})


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
