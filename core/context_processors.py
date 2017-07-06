from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'FOOTER_TAGS': settings.FOOTER_TAGS,
    }
