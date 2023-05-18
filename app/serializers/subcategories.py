from rest_framework import serializers

from app.models import SubCategory
from app.serializers.categories import CategorySerializer


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = SubCategory
        exclude = ["created_at"]
