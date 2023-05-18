from rest_framework import serializers

from app.models import Order, DeliveryCountries, OrderProduct
from app.serializers.basket import BasketSerializer


class DeliveryCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCountries
        exclude = ["created_at"]


class OrderProductSerializer(serializers.ModelSerializer):
    basket = BasketSerializer(many=False)

    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    delivery_city = DeliveryCountrySerializer(many=False)
    order_product_order = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        exclude = ["buy", ]
