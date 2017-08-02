#!/usr/bin/env python
# vim:ts=4:sw=4:et:ft=python
#
# Caching decorator for Django /jsi18n/
# http://wtanaka.com/django/jsi18ncache
#
# Copyright (C) 2009 Wesley Tanaka <http://wtanaka.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
TEN_YEARS = datetime.timedelta(days=3650)


def javascript_catalog(request, domain='djangojs', packages=None):
    """From https://github.com/wtanaka/django-jsi18ncache"""
    import django.views.i18n
    response = django.views.i18n.javascript_catalog(request, domain=domain, packages=packages)
    from django.utils.translation import check_for_language
    if request.GET and 'language' in request.GET and \
            check_for_language(request.GET['language']):
        expires = datetime.datetime.now() + TEN_YEARS
        response['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        response['Cache-Control'] = 'public'

    return response
