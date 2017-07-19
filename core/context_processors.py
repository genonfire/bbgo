from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'ADMIN_EMAIL': settings.ADMIN_EMAIL,
        'ADMIN_TWITTER': settings.ADMIN_TWITTER,
        'ENABLE_CODE_HIGHLIGHT': settings.ENABLE_CODE_HIGHLIGHT,
    }
