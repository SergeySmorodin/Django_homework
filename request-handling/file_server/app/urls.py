from django.urls import path, register_converter

from . import views, converters

register_converter(converters.DateConverter, 'date')


urlpatterns = [
    path('', views.file_list, name='file_list'), # Отображение списка файлов
    path('<date:date>/', views.file_list, name='file_list'), # Отображение списка файлов с фильтрацией по дате
    path('<str:name>/', views.file_content, name='file_content'), # Отображение содержимого файла
]
