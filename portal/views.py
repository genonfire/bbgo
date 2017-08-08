# -*- coding: utf-8 -*-
from math import ceil

from boards.models import Board
from core.utils import error_page, get_ipaddress

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext as _


def portal(request):
    """Portal"""
    return render(
        request,
        "portal/index.html",
    )
