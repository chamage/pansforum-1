"""M1 forms: account registration, authentication and basic profile details."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction

from .services import get_or_create_profile


class StyledFieldsMixin:
    def _style_fields(self):
        for field in self.fields.values():
            field.widget.attrs["class"] = "textarea" if isinstance(field.widget, forms.Textarea) else "input"
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("placeholder", field.label)


class RegisterForm(StyledFieldsMixin, UserCreationForm):
    email = forms.EmailField(label="Adres e-mail", required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ForumAuthenticationForm(StyledFieldsMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ProfileEditForm(StyledFieldsMixin, forms.Form):
    first_name = forms.CharField(label="Imię", max_length=150, required=False)
    last_name = forms.CharField(label="Nazwisko", max_length=150, required=False)
    email = forms.EmailField(label="Adres e-mail", required=False)
    bio = forms.CharField(label="O mnie", max_length=500, required=False, widget=forms.Textarea)

    def __init__(self, *args, user=None, **kwargs):
        if user is not None and not args and "initial" not in kwargs:
            profile = get_or_create_profile(user)
            kwargs["initial"] = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "bio": profile.bio,
            }
        super().__init__(*args, **kwargs)
        self._style_fields()

    @transaction.atomic
    def save(self, user):
        if not self.is_valid():
            raise ValueError("Cannot save an invalid profile form.")
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save(update_fields=["first_name", "last_name", "email"])
        profile = get_or_create_profile(user)
        profile.bio = self.cleaned_data["bio"]
        profile.save(update_fields=["bio", "updated_at"])
        return profile
