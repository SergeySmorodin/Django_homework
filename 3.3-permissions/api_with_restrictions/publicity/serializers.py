from rest_framework import serializers
from .models import Advertisement, AdvertisementStatusChoices
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serializer для пользователя """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """ Serializer для объявления """
    creator = UserSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', 'is_favorite')

    def create(self, validated_data):
        """ Метод для создания """
        # Установка значения поля создатель по умолчанию
        validated_data["creator"] = self.context["request"].user

        # Вызов метода validate для проверки данных
        self.validate(validated_data)

        # Создание объекта через родительский метод
        return super().create(validated_data)

    def validate(self, data):
        """ Метод для валидации. Вызывается при создании и обновлении """
        user = self.context["request"].user
        # Определяем текущий статус объявления (если оно обновляется)
        current_status = self.instance.status if self.instance else None
        # Получаем новый статус из данных или используем значение по умолчанию
        new_status = data.get("status", AdvertisementStatusChoices.OPEN)

        if new_status == AdvertisementStatusChoices.OPEN:
            # Получаем количество открытых объявлений пользователя
            open_ads_count = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN).count()

            # Если объявление обновляется и уже имеет статус OPEN, исключаем его из подсчёта
            if self.instance and current_status == AdvertisementStatusChoices.OPEN:
                open_ads_count -= 1

            if open_ads_count >= 10:
                raise serializers.ValidationError("У пользователя не может быть больше 10 открытых объявлений")

        return data

    def get_is_favorite(self, obj):
        """ Проверка, добавлено ли объявление в избранное текущим пользователем """
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False
