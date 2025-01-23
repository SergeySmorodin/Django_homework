# python manage.py shell

from books.models import Book


book1 = Book(name="Война и мир", author="Лев Толстой", pub_date="1869-01-01")
book1.save()

book2 = Book(name="1984", author="Джордж Оруэлл", pub_date="1949-06-08")
book2.save()

book3 = Book(name="Скотный двор", author="Джордж Оруэлл", pub_date="1945-08-17")
book3.save()

book4 = Book(name="В память о прошлом земли", author="Александр Блок", pub_date="1922-01-01")
book4.save()

book5 = Book(name="Мастер и Маргарита", author="Михаил Булгаков", pub_date="1967-11-01")
book5.save()

book6 = Book(name="Преступление и наказание", author="Федор Достоевский", pub_date="1866-01-01")
book6.save()

book7 = Book(name="Сто лет одиночества", author="Габриэль Гарсиа Маркес", pub_date="1967-05-30")
book7.save()

book8 = Book(name="Тихий Дон", author="Михаил Шолохов", pub_date="1940-01-01")
book8.save()