from rest_framework import serializers

from app.models import Product, ProductType, ProductCountry
from app.serializers.subcategories import SubCategorySerializer


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        exclude = ["created_at"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCountry
        exclude = ["created_at"]


class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=False, read_only=True)
    product_type = ProductTypeSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)

    is_liked = serializers.IntegerField(default=0)

    class Meta:
        model = Product
        fields = "__all__"
