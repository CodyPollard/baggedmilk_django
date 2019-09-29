from django import template

register = template.Library()


@register.filter
def inj_type(value):
    return type(value)


@register.filter
def inj_games_missed(value):
    games_missed = 0
    for record in value.split(','):
        try:
            games_missed += int(''.join(e for e in record.split(':')[-1] if e.isalnum()))
        except ValueError:
            pass
    return games_missed


@register.filter
def inj_count(value):
    inj_total = 0
    if ':' in value:
        for record in value.split(','):
            inj_total += 1
    else:
        return 0
    return inj_total


@register.filter
def format_name(value):
    name = ''
    for chunk in value.split('_'):
        name += (chunk.capitalize() + ' ')
    return name

