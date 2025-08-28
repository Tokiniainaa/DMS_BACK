from rest_framework import viewsets, permissions
from .models import Document
from .serializers import DocumentSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser


@method_decorator(csrf_exempt, name='dispatch')
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by("-uploaded_at")
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Document.objects.all().order_by("-uploaded_at")
        return Document.objects.filter(owner=user).order_by("-uploaded_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
