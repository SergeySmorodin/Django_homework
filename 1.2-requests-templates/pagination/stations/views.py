import csv
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    csv_file_path = settings.BUS_STATION_CSV

    with open(csv_file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        stations_list = list(reader) # Преобразуем в список словарей

    paginator = Paginator(stations_list, 10)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }

    return render(request, 'stations/index.html', context)
