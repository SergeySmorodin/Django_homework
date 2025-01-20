from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    phones = Phone.objects.all()

    # Сортировка
    sort_option = request.GET.get('sort', 'name')
    if sort_option == 'max_price':
        phones = phones.order_by('-price')
    elif sort_option == 'min_price':
        phones = phones.order_by('price')
    else:
        phones = phones.order_by('name')

    context = {
        'phones': phones
    }
    return render(request, 'catalog.html', context)


def show_product(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    context = {
        'phone': phone
    }
    return render(request, 'product.html', context)
