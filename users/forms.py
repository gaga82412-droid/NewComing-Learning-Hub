
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Email"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Nhập tên đăng nhập",
            "email": "Nhập địa chỉ email",
            "password1": "Nhập mật khẩu",
            "password2": "Nhập lại mật khẩu",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": placeholders.get(name, ""),
            })

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Tên đăng nhập hoặc Email"

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nhập tên đăng nhập hoặc email",
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Nhập mật khẩu",
        })

    def clean(self):
        username = self.data.get("username", "").strip()

        if "@" in username:
            user = User.objects.filter(
                email__iexact=username
            ).first()

            if user:
                data = self.data.copy()
                data["username"] = user.username
                self.data = data

        return super().clean()
