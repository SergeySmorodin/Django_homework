from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Student(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, blank=True, related_name='courses')

    def clean(self):
        student_count = self.students.count()
        if student_count >= settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f"Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}")

    def add_student(self, student):
        if self.students.count() >= settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(
                f"Курс уже достиг максимального числа студентов ({settings.MAX_STUDENTS_PER_COURSE}).")
        self.students.add(student)

    def __str__(self):
        return self.name
