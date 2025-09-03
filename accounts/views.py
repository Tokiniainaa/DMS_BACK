from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # ✅ Seul l'admin a accès aux routes

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role", "is_staff", "is_active"]
    search_fields = ["username", "email"]
    ordering_fields = ["username", "email", "role"]
    ordering = ["username"]

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

    # 🔹 Endpoint personnalisé pour récupérer l'utilisateur connecté
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    # 🔹 Endpoint pour récupérer tous les utilisateurs actifs (owners)
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def owners_list(self, request):
        """
        Retourne tous les utilisateurs actifs pour les filtres.
        Accessible à tous les utilisateurs connectés.
        """
        users = User.objects.filter(is_active=True)
        data = [{'id': u.id, 'username': u.username} for u in users]
        return Response(data)
