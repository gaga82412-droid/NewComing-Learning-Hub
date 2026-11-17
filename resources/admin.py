from django.contrib import admin
from .models import StudyResource


@admin.register(StudyResource)
class StudyResourceAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "created_at",
    )

    list_filter = ("category",)

    search_fields = (
        "title",
        "description",
    )