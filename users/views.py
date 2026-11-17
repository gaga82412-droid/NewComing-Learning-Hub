
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect("users:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Đăng nhập ngay sau khi đăng ký
            login(request, user)

            messages.success(
                request,
                "Đăng ký tài khoản thành công!"
            )

            return redirect("users:dashboard")

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {
        "form": form
    })


def login_view(request):

    if request.user.is_authenticated:
        return redirect("users:dashboard")

    if request.method == "POST":
        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(
                request,
                "Đăng nhập thành công!"
            )

            return redirect("users:dashboard")

    else:
        form = LoginForm(request)

    return render(request, "users/login.html", {
        "form": form
    })


@login_required(login_url="users:login")
def dashboard_view(request):

    return render(request, "users/dashboard.html")


def logout_view(request):

    if request.method == "POST":
        logout(request)

        messages.success(
            request,
            "Bạn đã đăng xuất thành công!"
        )

    return redirect("home:index")

@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")