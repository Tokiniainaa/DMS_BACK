from rest_framework import permissions


class IsNotViewer(permissions.BasePermission):
    """
    Empêche les utilisateurs avec rôle 'viewer' de créer des documents.
    """

    def has_permission(self, request, view):
        # Toujours autoriser les superusers
        if request.user and request.user.is_superuser:
            return True

        # Vérifier si c'est une création (action ou POST)
        if hasattr(view, "action") and view.action == "create":
            return getattr(request.user, "role", None) != "viewer"
        if request.method == "POST":
            return getattr(request.user, "role", None) != "viewer"

        return True
