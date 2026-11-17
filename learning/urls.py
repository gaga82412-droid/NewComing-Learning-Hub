
from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("quizzes/", views.quiz_list, name="quiz_list"),
    path("quizzes/<int:quiz_id>/", views.quiz_detail, name="quiz_detail"),
    path(
        "result/<int:attempt_id>/",
        views.quiz_result,
        name="quiz_result"
    ),
]
