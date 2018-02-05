# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from accounts.models import Profile

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


class SettingForm(forms.ModelForm):
    """Edit form for setting"""

    class Meta:
        """Meta for SettingForm"""

        model = Profile
        fields = {
            "alarm_interval", "alarm_board", "alarm_reply",
            "alarm_team", "alarm_full", "sense_client", "sense_slot"
        }

    def __init__(self, *args, **kwargs):
        """Init"""
        super(SettingForm, self).__init__(*args, **kwargs)
        self.fields['alarm_reply'].widget.attrs['checked'] = 'checked'
        self.fields['alarm_reply'].widget.attrs['disabled'] = True
        self.fields['alarm_full'].widget.attrs['checked'] = 'checked'
        self.fields['alarm_full'].widget.attrs['disabled'] = True


class UserInfoForm(forms.ModelForm):
    """Edit form for user info"""

    email = forms.EmailField(label='email', required=True)
    code = forms.CharField(label='code', required=False)
    first_name = forms.CharField(max_length=12, required=False)

    class Meta:
        """Meta for UserInfoForm"""

        model = Profile
        fields = {
            "portrait", "email", "code", "id1", "id2", "id3", "signature"
        }
        if settings.ENABLE_NICKNAME:
            fields.add("first_name")

    def __init__(self, *args, **kwargs):
        """Init"""
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email
        if settings.ENABLE_NICKNAME:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['first_name'].widget.attrs['maxlength'] = settings.ID_MAX_LENGTH
