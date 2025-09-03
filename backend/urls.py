from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from documents.views import DocumentViewSet, CategoryViewSet, PermissionViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r"documents", DocumentViewSet, basename="document")
router.register(r'categories', CategoryViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),

    # <-- inclure ton app accounts ici
    path("", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
