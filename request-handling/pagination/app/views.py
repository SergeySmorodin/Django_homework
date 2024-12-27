import csv
from urllib.parse import urlencode
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    file_path = settings.BUS_STATION_CSV
    bus_stations_list = []

    with open(file_path, encoding='cp1251') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bus_stations_list.append(row)

    paginator = Paginator(bus_stations_list, 10)
    page_number = int(request.GET.get('page', 1))
    bus_stations_page = paginator.get_page(page_number)

    current_page = bus_stations_page.number
    prev_page_url = None
    next_page_url = None

    if bus_stations_page.has_previous():
        prev_page_url = f"{reverse('bus_stations')}?{urlencode({'page': current_page - 1})}"

    if bus_stations_page.has_next():
        next_page_url = f"{reverse('bus_stations')}?{urlencode({'page': current_page + 1})}"

    context = {
        'bus_stations': bus_stations_page.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }

    return render(request, 'index.html', context)
