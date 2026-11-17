
from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "content", "order")
    list_filter = ("quiz",)
    search_fields = ("content",)
    inlines = [ChoiceInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "quiz",
        "score",
        "correct_answers",
        "total_questions",
        "completed_at",
    )
    list_filter = ("quiz", "completed_at")
    search_fields = ("user__username", "quiz__title")
    readonly_fields = (
        "user",
        "quiz",
        "score",
        "correct_answers",
        "total_questions",
        "completed_at",
    )
