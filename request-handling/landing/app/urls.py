from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('landing/', views.landing, name='landing'),
    path('end', views.index, name='index'),
    path('stats/', views.stats, name='stats'),
]
