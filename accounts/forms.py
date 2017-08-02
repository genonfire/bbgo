# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
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
        if settings.ENABLE_NICKNAME:
            fields.add("first_name")

    def __init__(self, *args, **kwargs):
        """Override maxlength"""
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = settings.ID_MAX_LENGTH
        if settings.ENABLE_NICKNAME:
            self.fields['first_name'].widget.attrs['maxlength'] = settings.ID_MAX_LENGTH
