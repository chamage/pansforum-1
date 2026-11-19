from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("ui-preview/", views.ui_preview, name="ui_preview"),
    path("ui-components/", views.ui_components, name="ui_components"),
]
