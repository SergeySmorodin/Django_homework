import datetime

# Конвертер для дат в формат YYYY-MM-DD
class DateConverter:
    regex = r'\d{4}-\d{2}-\d{2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        # для преобразования строки в объект date
        return datetime.datetime.strptime(value, self.format).date()

    def to_url(self, value):
        # объект date преобразует обратно в строку формата `YYYY-MM-DD`
        return value.strftime(self.format)

