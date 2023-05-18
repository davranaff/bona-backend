from rest_framework import serializers

from app.models import Basket
from app.serializers.products import ProductSerializer


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Basket
        fields = "__all__"
