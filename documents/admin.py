from .models import Permission
from django.contrib import admin
from .models import Document, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "uploaded_at")
    list_filter = ("category", "uploaded_at")
    search_fields = ("title", "owner__username")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "document", "permission")
    list_filter = ("permission",)
    search_fields = ("user__username", "document__title")
