# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Team, TeamReply

admin.site.register(Team)
admin.site.register(TeamReply)
