"""M1 account views. POST is required for any state-changing action."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import ForumAuthenticationForm, ProfileEditForm, RegisterForm
from .models import Profile
from .services import get_or_create_profile, register_account


class ForumLoginView(LoginView):
    authentication_form = ForumAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class ForumLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = register_account(form)
        login(request, user)
        return redirect("accounts:profile")
    return render(request, "accounts/register.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    current_profile = get_or_create_profile(request.user)
    form = ProfileEditForm(request.POST, user=request.user) if request.method == "POST" else ProfileEditForm(user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save(request.user)
        messages.success(request, "Zapisano zmiany.")
        return redirect("accounts:profile")
    role_label = (
        "Administrator" if request.user.is_superuser or current_profile.role == Profile.Role.ADMIN
        else "Moderator" if current_profile.role == Profile.Role.MODERATOR
        else "Student"
    )
    return render(request, "accounts/profile.html", {
        "form": form, "role_label": role_label,
    })
