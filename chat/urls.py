
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_page, name="index"),
    path(
        "get-response/",
        views.get_response,
        name="get_response"
    ),
]
