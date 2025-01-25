from django.contrib import admin

from .models import Article, Scope, Tag

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ScopeInlineFormset(BaseInlineFormSet):
    """Переопределяет метод clean, добавляет ограничение по основному тегу"""

    def clean(self):
        super().clean()
        main_count = 0
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data.get('is_main'):
                main_count += 1
        if main_count > 1:
            raise ValidationError('Только один тег может быть основным.')


class ScopeInline(admin.TabularInline):
    """Настройка отображения формы для модели Scope в админке"""
    model = Scope
    formset = ScopeInlineFormset
    extra = 3


# Регистрация модели Article в админке
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


# Регистрация модели Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
