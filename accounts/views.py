from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()  # récupère ton User personnalisé


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # ✅ Seul l'admin a accès aux routes

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role", "is_staff", "is_active"]  # filtrage par champs
    search_fields = ["username", "email"]  # recherche texte
    ordering_fields = ["username", "email", "role"]  # champs triables
    ordering = ["username"]  # tri par défaut

    def get_queryset(self):
        """Retourne tous les users sauf les superusers"""
        return User.objects.filter(is_superuser=False)

    def perform_create(self, serializer):
        """Autorise uniquement les admins à créer un user"""
        if not self.request.user.is_superuser and self.request.user.role != "admin":
            raise PermissionDenied("Seul un admin peut créer un utilisateur.")
        serializer.save()

    def perform_destroy(self, instance):
        """Autorise uniquement les admins à supprimer un user"""
        if not self.request.user.is_superuser and self.request.user.role != "admin":
            raise PermissionDenied(
                "Seul un admin peut supprimer un utilisateur.")
        instance.delete()

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="owners_list")
    def owners_list(self, request):
        """Retourne la liste de tous les utilisateurs (accessible uniquement par un admin)"""

        if not request.user.is_superuser and getattr(request.user, "role", None) != "admin":
            raise PermissionDenied(
                "Seul un admin peut voir la liste des utilisateurs.")

        # 🔍 Récupérer tous les users (sauf superuser si tu veux)
        owners = User.objects.filter(is_superuser=False)

        serializer = self.get_serializer(owners, many=True)
        return Response(serializer.data)
