
from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên bài trắc nghiệm")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    is_published = models.BooleanField(default=False, verbose_name="Đã xuất bản")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bài trắc nghiệm"
        verbose_name_plural = "Bài trắc nghiệm"

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    content = models.TextField(verbose_name="Nội dung câu hỏi")
    order = models.PositiveIntegerField(default=1, verbose_name="Thứ tự")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Câu hỏi"
        verbose_name_plural = "Câu hỏi"

    def __str__(self):
        return f"{self.quiz.title} - Câu {self.order}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    content = models.CharField(max_length=500, verbose_name="Nội dung đáp án")
    is_correct = models.BooleanField(default=False, verbose_name="Đáp án đúng")

    class Meta:
        verbose_name = "Đáp án"
        verbose_name_plural = "Đáp án"

    def __str__(self):
        return self.content


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="learning_quiz_attempts"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts"
    )
    score = models.FloatField(default=0, verbose_name="Điểm số")
    correct_answers = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]
        verbose_name = "Lượt làm bài"
        verbose_name_plural = "Lượt làm bài"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score} điểm)"
