from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # on expose le password en write_only pour qu'il soit envoyé mais jamais lu
    password = serializers.CharField(
        write_only=True, required=True, max_length=150)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role",
                  "is_staff", "is_superuser", "is_active", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # ⚡ important pour hacher le mot de passe
        user.save()
        return user
