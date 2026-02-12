from django import forms
from django.contrib.auth.models import User
from .models import Complaint

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["title", "description"]

class AdminUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["status", "admin_note"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
