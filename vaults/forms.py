# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from .models import Key, Vault


class CheckKeyForm(forms.ModelForm):
    """Key for vaults"""

    class Meta:
        """Meta for KeyEditForm"""

        model = Key
        fields = ('masterkey',)

    def __init__(self, *args, **kwargs):
        """Override maxlength"""
        super(CheckKeyForm, self).__init__(*args, **kwargs)
        self.fields['masterkey'].widget.attrs['maxlength'] = settings.MASTERKEY_LENGTH


class NewKeyForm(forms.ModelForm):
    """Key for vaults"""

    class Meta:
        """Meta for KeyEditForm"""

        model = Key
        fields = ('masterkey',)

    def __init__(self, *args, **kwargs):
        """Override maxlength"""
        super(NewKeyForm, self).__init__(*args, **kwargs)
        self.fields['masterkey'].widget.attrs['maxlength'] = settings.MASTERKEY_LENGTH


class KeyEditForm(forms.ModelForm):
    """Key for vaults"""

    current_key = forms.CharField(required=True)

    class Meta:
        """Meta for KeyEditForm"""

        model = Key
        fields = ('current_key', 'masterkey',)

    def __init__(self, *args, **kwargs):
        """Override maxlength"""
        super(KeyEditForm, self).__init__(*args, **kwargs)
        self.fields['current_key'].widget.attrs['maxlength'] = settings.MASTERKEY_LENGTH
        self.fields['masterkey'].widget.attrs['maxlength'] = settings.MASTERKEY_LENGTH


class VaultEditForm(forms.ModelForm):
    """Vault for vaults"""

    class Meta:
        """Meta for VaultEditForm"""

        model = Vault
        exclude = ('user', 'created_at', 'order',)
