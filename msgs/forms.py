# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Msg


class MsgForm(forms.ModelForm):
    """Form for Message"""

    class Meta:
        """Meta for ModelForm"""

        model = Msg
        exclude = (
            'sender', 'recipient', 'sender_status', 'recipient_status', 'created_at', 'ip'
        )
