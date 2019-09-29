from datetime import timedelta, datetime
from django.forms import formset_factory
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import TimerForm, PasteComparisonForm, InjuryUpdateForm, PollQuestionForm, PollChoiceForm
from .models import Timer, DucksInjury, IndividualPlayer, RegularSeasonGame, IndividualGame
import re, pdb


# Create your views here.
def index(request):
    return render(request, 'milk/index.html')


def milkbot(request):
    return render(request, 'milk/milkbot.html')


def poll(request):
    question_form = PollQuestionForm(request.POST or None)
    choice_form = PollChoiceForm(request.POST or None)

    # new_poll_set = formset_factory(PollQuestionForm, PollChoiceForm)
    # If the form is valid
    if question_form.is_valid() and choice_form.is_valid():
        question_form = question_form.save(commit=False)
        choice_form = choice_form.save(commit=False)

        # Save forms
        question_form.save()
        choice_form.save()
        return redirect('poll')
    return render(request, 'milk/poll.html', {'question_form' : question_form,
                                              'choice_form' : choice_form})


def wwdli_success(request):
    injury_list = DucksInjury.objects.filter(published=True).order_by('-last_injury')
    latest_injury = injury_list[0]
    # Get all currently injured players
    injured_players = IndividualPlayer.objects.filter(healthy=False).order_by('-salary')
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
    try:
        injury_list = DucksInjury.objects.filter(published=True).order_by('-last_injury')
        latest_injury = injury_list[0]
    except IndexError:
        latest_injury = ['']
    # Get all currently injured players
    injured_players = IndividualPlayer.objects.filter(healthy=False).order_by('-salary')
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
        if i.pos.lower().split(',')[0] in forward:
            fwd += 1
        elif i.pos.lower().split(',')[0] in defense:
            de += 1
        elif i.pos.lower() == 'g':
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


def wwdli_roster_ducks(request):
    all_players = IndividualPlayer.objects.all()
    # all_games = IndividualGame.objects.all()
    all_injuries = DucksInjury.objects.all()

    players = []

    for player in all_players:
        inj_count = 0
        for inj in all_injuries.filter(player=player):
            inj_count += 1
        players.append([player, inj_count])
        # player_dict['inj_count'] = inj_count

    # pdb.set_trace()

    return render(request, 'milk/wwdli-roster-ducks.html', {'players': players})


def wwdli_player(request, player_name):
    player = IndividualPlayer.objects.get(name=player_name)
    game_list = RegularSeasonGame.objects.filter(player=player)
    injury_list = DucksInjury.objects.filter(player=player)
    # Stats
    goals, assists, pm, pim, shots, shifts, toi, blocks, hits = 0, 0, 0, 0, 0, 0, 0, 0, 0
    # Get season total stats
    for game in game_list:
        goals += game.goals
        assists += game.assists
        pm += game.pm
        pim += game.pim
        shots += game.shots
        shifts += game.shifts
        toi += game.toi
        blocks += game.blocks
        hits += game.hits
    # injury_list = DucksInjury.objects.filter(published=True).order_by('-last_injury')
    avg_shifts = shifts/game_list.count()
    avg_toi = toi/game_list.count()
    player_stats = [goals, assists, pm, pim, shots, hits, blocks, avg_shifts, avg_toi]
    if player is None:
        return HttpResponseNotFound('<h1>Player not found. Check rosters for available players.</h1>')
    return render(request, 'milk/wwdli-player-breakdown.html', {'player': player,
                                                                'injury_list': injury_list,
                                                                'player_stats': player_stats})


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


def jeff_xml(request):
    return render(request, 'milk/jeff-xml.html')
