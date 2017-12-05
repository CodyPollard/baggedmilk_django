from datetime import timedelta, datetime

from django.http import Http404
from django.shortcuts import render, redirect
from .forms import TimerForm, PasteComparisonForm, InjuryUpdateForm
from .models import Timer, DucksInjury, DucksPlayer
from django.core.mail import send_mail
import re


# Create your views here.
def index(request):
    return render(request, 'milk/index.html')


def milkbot(request):
    return render(request, 'milk/milkbot.html')


def wwdli_success(request):
    injury_list = DucksInjury.objects.filter(published=True).order_by('-last_injury')
    latest_injury = injury_list[0]
    # Get all currently injured players
    injured_players = DucksPlayer.objects.filter(healthy=False).order_by('-salary')
    # Get stats for display in template
    salary_hit = 0
    forward = ['lw', 'c', 'rw']
    defense = ['ld', 'rd']
    fwd, de, goalie = 0, 0, 0
    youth, regular, old = 0, 0, 0
    # Loop through players to get stats
    for i in injured_players:
        # Get total salary hit
        salary_hit += i.salary
        # Get positions
        if i.position.lower().split(',')[0] in forward:
            fwd += 1
        elif i.position.lower().split(',')[0] in defense:
            de += 1
        elif i.position.lower() == 'g':
            goalie += 1
        # Get ages
        if i.age <= 25:
            youth += 1
        elif 25 < i.age < 35:
            regular += 1
        elif i.age >= 35:
            old += 1

    # Lists to use in template
    ages = [youth, regular, old]
    positions = [fwd, de, goalie]
    return render(request, 'milk/wwdli-success.html', {'latest_injury': latest_injury,
                                                       'injury_list': injury_list,
                                                       'injured_players': injured_players,
                                                       'salary_hit': salary_hit,
                                                       'ages': ages,
                                                       'positions': positions})


def wwdli_injury(request, injury_id):
    try:
        injury = DucksInjury.objects.get(pk=injury_id)
        injury_list = DucksInjury.objects.filter(published=True).order_by('-last_injury')
        player = injury.player
    except DucksInjury.DoesNotExist:
        raise Http404("Injury Doesn't Exist.")
    return render(request, 'milk/wwdli-injury.html', {'injury': injury,
                                                      'injury_list': injury_list,
                                                      'player': player})


def wwdli(request):
    # Get all published injuries
    injury_list = DucksInjury.objects.filter(published=True).order_by('-last_injury')
    latest_injury = injury_list[0]
    # Get all currently injured players
    injured_players = DucksPlayer.objects.filter(healthy=False).order_by('-salary')
    # Get stats for display in template
    salary_hit = 0
    forward = ['lw', 'c', 'rw']
    defense = ['ld', 'rd']
    fwd, de, goalie = 0, 0, 0
    youth, regular, old = 0, 0, 0
    # Loop through players to get stats
    for i in injured_players:
        # Get total salary hit
        salary_hit += i.salary
        # Get positions
        if i.position.lower().split(',')[0] in forward:
            fwd += 1
        elif i.position.lower().split(',')[0] in defense:
            de += 1
        elif i.position.lower() == 'g':
            goalie += 1
        # Get ages
        if i.age <= 25:
            youth += 1
        elif 25 < i.age < 35:
            regular += 1
        elif i.age >= 35:
            old += 1

    # Lists to use in template
    ages = [youth, regular, old]
    positions = [fwd, de, goalie]
    # Form
    form = InjuryUpdateForm(request.POST or None)
    # If the form is valid, create new injury object with status defaulted to unpublished
    if form.is_valid():
        inj_form = form.save(commit=False)
        inj_form.save()
        return redirect('wwdli-success')

    return render(request, 'milk/wwdli.html', {'latest_injury': latest_injury, 'form': form,
                                               'injury_list': injury_list,
                                               'injured_players': injured_players,
                                               'salary_hit': salary_hit,
                                               'ages': ages,
                                               'positions': positions})


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
