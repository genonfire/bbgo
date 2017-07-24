from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'DEBUG': settings.DEBUG,
        'SITE_NAME': settings.SITE_NAME,
        'ADMIN_EMAIL': settings.ADMIN_EMAIL,
        'ADMIN_TWITTER': settings.ADMIN_TWITTER,
        'ENABLE_CODE_HIGHLIGHT': settings.ENABLE_CODE_HIGHLIGHT,
        'REPLY_TEXT_MAX': settings.REPLY_TEXT_MAX,
        'REPLY_IMAGE_AVAILABLE': settings.REPLY_IMAGE_AVAILABLE,
        'REPLY_IMAGE_SIZE_LIMIT': settings.REPLY_IMAGE_SIZE_LIMIT,
    }
