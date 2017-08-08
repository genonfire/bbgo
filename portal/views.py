# -*- coding: utf-8 -*-
from django.shortcuts import render


def portal(request):
    """Portal"""
    return render(
        request,
        "portal/index.html",
    )
