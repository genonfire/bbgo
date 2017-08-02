from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'DEBUG': settings.DEBUG,
        'APP_VERSION': settings.APP_VERSION,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_LOGO': settings.SITE_LOGO,
        'SITE_INFO': settings.SITE_INFO,
        'ADMIN_EMAIL': settings.ADMIN_EMAIL,
        'ID_MIN_LENGTH': settings.ID_MIN_LENGTH,
        'ID_MAX_LENGTH': settings.ID_MAX_LENGTH,
        'ENABLE_NICKNAME': settings.ENABLE_NICKNAME,
        'REPLY_TEXT_MAX': settings.REPLY_TEXT_MAX,
        'REPLY_IMAGE_AVAILABLE': settings.REPLY_IMAGE_AVAILABLE,
        'REPLY_IMAGE_SIZE_LIMIT': settings.REPLY_IMAGE_SIZE_LIMIT,
        'ENABLE_CODE_HIGHLIGHT': settings.ENABLE_CODE_HIGHLIGHT,
        'ENABLE_MARK_KEYWORD': settings.ENABLE_MARK_KEYWORD,
    }
