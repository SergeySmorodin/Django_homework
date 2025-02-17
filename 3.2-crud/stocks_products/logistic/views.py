from rest_framework.viewsets import ModelViewSet
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']  # Поля для поиска


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all().order_by('address')
    serializer_class = StockSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            # Ищем склады, у которых есть продукты с совпадением в title или description
            queryset = queryset.filter(
                Q(positions__product__title__icontains=search_query) |
                Q(positions__product__description__icontains=search_query)
            ).distinct()
        return queryset
