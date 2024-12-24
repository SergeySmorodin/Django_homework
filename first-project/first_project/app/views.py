import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.http import JsonResponse


def home_view(request):
    template_name = 'app/home.html'

    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    context = {
        'pages': pages
    }

    return render(request, template_name, context)


def time_view(request):
    template_name = 'app/time.html'

    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime("%H:%M:%S")

    context = {
        'time': formatted_time
    }

    return render(request, template_name, context)


def get_time(request):
    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime("%H:%M:%S")

    return JsonResponse({'time': formatted_time})


def workdir_view(request):
    template_name = 'app/workdir.html'

    current_directory = os.getcwd()  # получение пути к рабочему каталогу
    files = os.listdir(current_directory)  # возвращает список всех файлов
    files = [f for f in files if os.path.isfile(os.path.join(current_directory, f))]  # исключаем папки

    context = {
        'files': files
    }

    return render(request, template_name, context)
