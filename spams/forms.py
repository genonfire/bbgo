# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import IP, Word


class SpamIPEditForm(forms.ModelForm):
    """IP for spam"""

    class Meta:
        """Meta for ModelForm"""

        model = IP
        fields = ('ip',)


class SpamWordEditForm(forms.ModelForm):
    """Word for spam"""

    class Meta:
        """Meta for ModelForm"""

        model = Word
        fields = ('word',)
