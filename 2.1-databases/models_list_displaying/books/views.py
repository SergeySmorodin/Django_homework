from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Book
from django.core.paginator import Paginator
from datetime import timedelta

def books_view(request):
    books = Book.objects.all()
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'books': page_obj}
    return render(request, 'books/books_list.html', context)

def books_by_date_view(request, pub_date):
    date = parse_date(pub_date)
    books = Book.objects.filter(pub_date=date)
    previous_date = date - timedelta(days=1)
    next_date = date + timedelta(days=1)

    context = {
        'books': books,
        'previous_date': previous_date,
        'next_date': next_date,
    }
    return render(request, 'books/books_by_date.html', context)
