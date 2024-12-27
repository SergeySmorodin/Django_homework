import datetime
import os
from django.conf import settings
from django.shortcuts import render


def file_list(request, date=None):
    files_path = settings.FILES_PATH
    template_name = 'index.html'

    files = []
    for filename in os.listdir(files_path):
        filepath = os.path.join(files_path, filename)
        if os.path.isfile(filepath):
            ctime = datetime.datetime.fromtimestamp(os.path.getctime(filepath))  # время создания файла
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))  # время последнего изменения

            files.append({
                'name': filename,
                'ctime': ctime,
                'mtime': mtime,
            })

    context = {
        'files': files,
        'date': date
    }

    return render(request, template_name, context)


def file_content(request, name):
    template_name = 'file_content.html'
    file_path = os.path.join(settings.FILES_PATH, name)

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
    except FileNotFoundError:
        file_content = 'Файл не найден.'

    context = {'file_name': name, 'file_content': file_content}

    return render(request, template_name, context)
