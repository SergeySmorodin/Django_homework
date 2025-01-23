from django.test import TestCase

from books.models import Book


class BookModelTest(TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.book1 = Book.objects.create(name="Война и мир", author="Лев Толстой", pub_date="1869-01-01")
        self.book2 = Book.objects.create(name="1984", author="Джордж Оруэлл", pub_date="1949-06-08")
        self.book3 = Book.objects.create(name="Скотный двор", author="Джордж Оруэлл", pub_date="1945-08-17")
        self.book4 = Book.objects.create(name="В память о прошлом земли", author="Александр Блок",
                                         pub_date="1922-01-01")

    def test_books_created(self):
        # Проверяем, что книги созданы и данные корректны
        self.assertEqual(Book.objects.count(), 4)

        book1 = Book.objects.get(name="Война и мир")
        self.assertEqual(book1.author, "Лев Толстой")
        self.assertEqual(book1.pub_date.strftime("%Y-%m-%d"), "1869-01-01")

        book2 = Book.objects.get(name="1984")
        self.assertEqual(book2.author, "Джордж Оруэлл")
        self.assertEqual(book2.pub_date.strftime("%Y-%m-%d"), "1949-06-08")

        book3 = Book.objects.get(name="Скотный двор")
        self.assertEqual(book3.author, "Джордж Оруэлл")
        self.assertEqual(book3.pub_date.strftime("%Y-%m-%d"), "1945-08-17")

        book4 = Book.objects.get(name="В память о прошлом земли")
        self.assertEqual(book4.author, "Александр Блок")
        self.assertEqual(book4.pub_date.strftime("%Y-%m-%d"), "1922-01-01")
