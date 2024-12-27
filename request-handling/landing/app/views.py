from collections import Counter
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

counter_show = Counter()
counter_click = Counter()


def home_view(request):
    template_name = 'home.html'

    pages = {
        'Альтернативная версия': reverse('landing') + f'?ab-test-arg=test',
        'Оригинальная версия': reverse('landing') + f'?ab-test-arg=original',
    }

    context = {
        'pages': pages
    }

    return render(request, template_name, context)


def index(request):
    from_landing = request.GET.get('from-landing')

    if from_landing:
        counter_click[from_landing] += 1

    return render(request, 'index.html')


def landing(request):
    ab_test_arg = request.GET.get('ab-test-arg')

    if ab_test_arg == 'test':
        counter_show['test'] += 1
        template_name = 'landing_alternate.html'
    else:
        counter_show['original'] += 1
        template_name = 'landing.html'

    return render(request, template_name)


def stats(request):
    original_shows = counter_show['original']
    test_shows = counter_show['test']

    original_clicks = counter_click['original']
    test_clicks = counter_click['test']

    original_conversion = (original_clicks / original_shows) if original_shows > 0 else 0
    test_conversion = (test_clicks / test_shows) if test_shows > 0 else 0

    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
