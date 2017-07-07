from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'ENABLE_CODE_HIGHLIGHT': settings.ENABLE_CODE_HIGHLIGHT,
        'FOOTER_TAGS': settings.FOOTER_TAGS,
    }
