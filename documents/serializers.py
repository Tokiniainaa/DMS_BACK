from .models import Category
from rest_framework import serializers
from .models import Document


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
            "owner"           # Important : owner est read_only
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
