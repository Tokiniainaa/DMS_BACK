from .models import Permission
from .models import Category
from rest_framework import serializers
from .models import Document
from accounts.models import User


class DocumentSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(
        source="owner.username", read_only=True)
    category_name = serializers.CharField(
        source="category.name", read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "uploaded_at",
            "owner",           # Ne sera pas envoyé depuis le front
            "owner_username",
            "category",
            "category_name"
        ]
        read_only_fields = [
            "uploaded_at",
            "owner_username",
            "category_name",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


# serializers.py


class PermissionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(
        source="user.username", read_only=True)
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),  # 👈 utilise ton User personnalisé
        slug_field='username'
    )

    class Meta:
        model = Permission
        fields = ['id', 'document', 'user', 'permission', 'user_username']
