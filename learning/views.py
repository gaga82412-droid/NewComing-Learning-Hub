
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg, Count

from .models import Quiz, QuizAttempt


@login_required
def dashboard(request):
    user_attempts = QuizAttempt.objects.filter(user=request.user)

    total_quizzes = Quiz.objects.filter(is_published=True).count()
    total_attempts = user_attempts.count()

    average_score = user_attempts.aggregate(
        average=Avg("score")
    )["average"] or 0

    recent_attempts = user_attempts.select_related(
        "quiz"
    )[:5]

    context = {
        "total_quizzes": total_quizzes,
        "total_attempts": total_attempts,
        "average_score": round(average_score, 2),
        "recent_attempts": recent_attempts,
    }

    return render(request, "learning/dashboard.html", context)


@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(
        is_published=True
    ).annotate(
        total_questions=Count("questions")
    )

    return render(
        request,
        "learning/quiz_list.html",
        {"quizzes": quizzes}
    )


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(
        Quiz,
        id=quiz_id,
        is_published=True
    )

    questions = quiz.questions.prefetch_related("choices")

    if not questions.exists():
        messages.warning(request, "Bài trắc nghiệm này chưa có câu hỏi.")
        return redirect("learning:quiz_list")

    if request.method == "POST":
        correct_answers = 0
        total_questions = questions.count()

        for question in questions:
            selected_id = request.POST.get(
                f"question_{question.id}"
            )

            if not selected_id:
                continue

            correct_choice = question.choices.filter(
                id=selected_id,
                is_correct=True
            ).exists()

            if correct_choice:
                correct_answers += 1

        score = (
            correct_answers / total_questions * 10
            if total_questions else 0
        )

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=round(score, 2),
            correct_answers=correct_answers,
            total_questions=total_questions,
        )

        return redirect(
            "learning:quiz_result",
            attempt_id=attempt.id
        )

    return render(
        request,
        "learning/quiz_detail.html",
        {
            "quiz": quiz,
            "questions": questions,
        }
    )


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(
        QuizAttempt.objects.select_related("quiz", "user"),
        id=attempt_id,
        user=request.user
    )

    return render(
        request,
        "learning/quiz_result.html",
        {"attempt": attempt}
    )
