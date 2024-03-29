from rest_framework import serializers

from app.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["created_at"]
