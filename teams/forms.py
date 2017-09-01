# -*- coding: utf-8 -*-

from django import forms

from .models import Team, TeamReply


class TeamEditForm(forms.ModelForm):
    """Form for team"""

    class Meta:
        """Meta for ModelForm"""

        CATEGORY = (
        )
        SLOT_CHOICE = (
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
        )
        model = Team
        exclude = (
            'table', 'user', 'created_at', 'modified_at', 'ip',
            'view_count', 'reply_count', 'slot', 'slot_users'
        )
        widgets = {
            'subject': forms.TextInput(
                attrs={'placeholder': u'제목을 입력해 주세요.'}
            ),
            'category': forms.Select(choices=CATEGORY),
            'slot_total': forms.Select(choices=SLOT_CHOICE),
        }

    def __init__(self, *args, **kwargs):
        """Init"""
        self.user = kwargs.pop('user', None)
        super(TeamEditForm, self).__init__(*args, **kwargs)


class TeamReplyEditForm(forms.ModelForm):
    """Form for reply"""

    class Meta:
        """Meta for ModelForm"""

        model = TeamReply
        exclude = (
            'reply_id', 'reply_to', 'status', 'user',
            'created_at', 'modified_at', 'ip',
        )

    def __init__(self, *args, **kwargs):
        """Init"""
        self.user = kwargs.pop('user', None)
        super(TeamReplyEditForm, self).__init__(*args, **kwargs)
