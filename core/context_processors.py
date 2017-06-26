from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'FOOTER_TAGS': settings.FOOTER_TAGS,
    }
