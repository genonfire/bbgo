# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django_summernote.widgets import SummernoteWidget

from .models import Blog, Comment


class BlogEditForm(forms.ModelForm):
    """Form for blog"""

    class Meta:
        """Meta for ModelForm"""

        CATEGORY = (
        )
        model = Blog
        exclude = (
            'user', 'created_at', 'modified_at', 'ip',
            'view_count', 'comment_count', 'like_count', 'like_users',
        )
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': _('Enter title here.')}
            ),
            'tags': forms.TextInput(
                attrs={'placeholder': _('Enter comma separated tags here.')}
            ),
            'category': forms.Select(choices=CATEGORY),
            'content': SummernoteWidget(),
        }

    def __init__(self, *args, **kwargs):
        """Init"""
        self.user = kwargs.pop('user', None)
        super(BlogEditForm, self).__init__(*args, **kwargs)


class CommentEditForm(forms.ModelForm):
    """Form for comment"""

    class Meta:
        """Meta for ModelForm"""

        model = Comment
        exclude = (
            'comment_id', 'status', 'user', 'created_at', 'modified_at', 'ip',
        )

    def __init__(self, *args, **kwargs):
        """Init"""
        self.user = kwargs.pop('user', None)
        super(CommentEditForm, self).__init__(*args, **kwargs)
