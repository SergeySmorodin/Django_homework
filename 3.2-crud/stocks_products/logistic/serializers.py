from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')  # Извлекаем данные о позициях
        stock = super().create(validated_data)  # Создаём склад

        # Заполняем таблицу StockProduct
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')  # Извлекаем данные о позициях
        stock = super().update(instance, validated_data)  # Обновляем склад

        # Обновляем или создаём позиции
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={'quantity': position['quantity'], 'price': position['price']}
            )

        return stock
