from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.ForumLoginView.as_view(), name="login"),
    path("logout/", views.ForumLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
