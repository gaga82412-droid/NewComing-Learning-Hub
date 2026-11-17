
from django.shortcuts import render
from django.db.models import Q
from .models import StudyResource


def resource_list(request):

    resources = StudyResource.objects.all()

    keyword = request.GET.get("q", "")
    category = request.GET.get("category", "")

    if keyword:
        resources = resources.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    if category:
        resources = resources.filter(category=category)

    return render(
        request,
        "resources/index.html",
        {
            "resources": resources,
            "keyword": keyword,
            "selected_category": category,
            "categories": StudyResource.CATEGORY_CHOICES
        }
    )
