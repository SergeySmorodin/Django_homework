from django.contrib import admin

from .models import Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    search_fields = ('name',)
    list_filter = ('group',)
    fields = ('name', 'group', 'teachers')  # Определение порядка полей в форме редактирования
    filter_horizontal = ('teachers',)  # Удобный вид для выбора нескольких преподавателей
    actions = ['make_group_b']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject')


