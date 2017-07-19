# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """Edit form for sign up"""

    email = forms.EmailField(label='email', required=True)
    code = forms.CharField(label='code', required=False)

    class Meta:
        """Meta for RegistrationForm"""

        model = User
        fields = {"username", "email", "code"}
