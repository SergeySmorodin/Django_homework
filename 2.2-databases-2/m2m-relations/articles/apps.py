from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    """Настройка отображения имени в админке"""
    name = 'articles'
    verbose_name = 'Новости' # имя будет использоваться в админке
