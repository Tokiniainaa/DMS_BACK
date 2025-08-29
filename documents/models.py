import uuid
from django.db import models
from django.conf import settings


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Relations
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # ou CASCADE selon ton choix
        null=False,
        blank=False,
        related_name="documents"
    )

    def __str__(self):
        return f"{self.title} ({self.owner.username})"


class Permission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Lecture'),
        ('write', 'Écriture'),
        ('delete', 'Suppression'),
        ('download', 'Téléchargement'),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.permission} - {self.document.title}"
