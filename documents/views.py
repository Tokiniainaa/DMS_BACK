from rest_framework import viewsets, permissions
from .models import Document, Category
from .permissions import IsNotViewer
from .serializers import DocumentSerializer, CategorySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


@method_decorator(csrf_exempt, name='dispatch')
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by("-uploaded_at")
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotViewer]
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "category__name": ["exact"],    # si category est FK
        "owner__username": ["iexact"],   # filtrage par username
        "uploaded_at": ["gte", "lte"],  # filtrage par plage de datesl
    }
    search_fields = ["title"]
    ordering_fields = ["title", "uploaded_at"]
    ordering = ["uploaded_at"]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Document.objects.all().order_by("-uploaded_at")
        return Document.objects.filter(owner=user).order_by("-uploaded_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
