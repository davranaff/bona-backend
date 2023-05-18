from rest_framework import serializers

from app.models import Wishlist
from app.serializers.products import ProductSerializer


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Wishlist
        fields = "__all__"
