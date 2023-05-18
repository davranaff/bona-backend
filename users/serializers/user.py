from rest_framework import serializers

from users.models import User, Email


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["id", "email"]


class UserSerializer(serializers.ModelSerializer):
    custom_email = EmailSerializer(read_only=True, many=False)

    class Meta:
        model = User
        exclude = (
            "first_name", "last_name", "password", "email", "is_staff", "is_active", "groups", "user_permissions",
            "created_at", "last_login")
