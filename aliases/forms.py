# -*- coding: utf-8 -*-
from django import forms

from .models import Alias


class AliasEditForm(forms.ModelForm):
    """Alias for Alias"""

    class Meta:
        """Meta for ModelForm"""

        model = Alias
        fields = ('name', 'url')
