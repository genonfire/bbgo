# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext as _
from django_summernote.widgets import SummernoteWidget

from .models import Paper


class PaperEditForm(forms.ModelForm):
    """Paper for Papers"""

    support_names = forms.CharField(required=False)
    notify_names = forms.CharField(required=False)

    class Meta:
        """Meta for ModelForm"""

        model = Paper
        fields = ('title', 'content', 'files', 'approver', 'support_names', 'notify_names',)
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': _('Enter title here.')}
            ),
            'content': SummernoteWidget(),
            'files': forms.ClearableFileInput(attrs={'multiple': True}),
            'approver': forms.TextInput(),
        }
