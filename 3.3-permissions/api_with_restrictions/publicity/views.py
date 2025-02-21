from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advertisement, Favorite, AdvertisementStatusChoices
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsAdminOrOwner

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

class AdvertisementViewSet(ModelViewSet):
    """ ViewSet для объявлений """
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [UserRateThrottle, AnonRateThrottle]


    def get_permissions(self):
        """ Получение прав для действий """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # Только аутентифицированные пользователи (админы или владельцы) могут изменять или удалять объявления
            return [IsAuthenticated(), IsAdminOrOwner()]
        return []

    def get_queryset(self):
        """ Фильтрация объявлений """
        queryset = super().get_queryset()
        user = self.request.user

        # Если пользователь аутентифицирован, показываем его черновики
        if user.is_authenticated:
            queryset = queryset.filter(
                Q(status=AdvertisementStatusChoices.OPEN) |
                Q(status=AdvertisementStatusChoices.CLOSED) |
                Q(creator=user, status=AdvertisementStatusChoices.DRAFT)
            )
        else:
            # Для анонимных пользователей показываем только OPEN и CLOSED
            queryset = queryset.filter(
                Q(status=AdvertisementStatusChoices.OPEN) |
                Q(status=AdvertisementStatusChoices.CLOSED)
            )

        # Фильтрация по избранным объявлениям
        if self.request.query_params.get('favorites') == 'true' and user.is_authenticated:
            queryset = queryset.filter(favorites__user=user)

        return queryset

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Добавление/удаление объявления в избранное."""
        advertisement = get_object_or_404(Advertisement, id=pk)
        user = request.user

        # Автор не может добавить своё объявление в избранное
        if advertisement.creator == user:
            return Response(
                {"detail": "Вы не можете добавить своё объявление в избранное"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            # Добавление в избранное
            Favorite.objects.get_or_create(user=user, advertisement=advertisement)
            return Response({"detail": "Объявление добавлено в избранное"}, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            # Удаление из избранного
            favorite = Favorite.objects.filter(user=user, advertisement=advertisement).first()
            if favorite:
                favorite.delete()
                return Response({"detail": "Объявление удалено из избранного"}, status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"detail": "Объявление не найдено в избранном"},
                status=status.HTTP_404_NOT_FOUND
            )
