# -*- coding: utf-8 -*-

from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Board


class BoardEditForm(forms.ModelForm):
    """Form for board"""

    class Meta:
        """Meta for ModelForm"""

        CATEGORY = (
        )
        model = Board
        exclude = (
            'table', 'user', 'created_at', 'modified_at', 'ip',
            'view_count', 'like_count', 'dislike_count', 'reply_count',
            'like_users', 'dislike_users', 'replies',
        )
        widgets = {
            'subject': forms.TextInput(
                attrs={'placeholder': u'제목을 입력해 주세요.'}
            ),
            'reference': forms.TextInput(
                attrs={'placeholder': u'출처가 있으면 입력해 주세요.'}
            ),
            'category': forms.Select(choices=CATEGORY),
            'content': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        """Init"""
        self.user = kwargs.pop('user', None)
        # self.base_fields['status'].initial = '1normal'
        super(BoardEditForm, self).__init__(*args, **kwargs)
