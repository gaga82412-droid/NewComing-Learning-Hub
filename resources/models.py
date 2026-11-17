
from django.db import models


class StudyResource(models.Model):

    CATEGORY_CHOICES = [
        ("python", "Lập trình Python"),
        ("django", "Lập trình Django"),
        ("web", "HTML, CSS, JavaScript"),
        ("database", "Cơ sở dữ liệu"),
        ("network", "Mạng máy tính"),
        ("other", "Khác"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other"
    )
    description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    file = models.FileField(
        upload_to="documents/",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
