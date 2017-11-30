from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'ADMIN_EMAIL': settings.ADMIN_EMAIL,
        'APP_VERSION': settings.APP_VERSION,
        'DEBUG': settings.DEBUG,
        'ENABLE_CODE_HIGHLIGHT': settings.ENABLE_CODE_HIGHLIGHT,
        'ENABLE_MARK_KEYWORD': settings.ENABLE_MARK_KEYWORD,
        'ENABLE_NICKNAME': settings.ENABLE_NICKNAME,
        'HOT_THRESHOLD': settings.HOT_THRESHOLD,
        'ID_MIN_LENGTH': settings.ID_MIN_LENGTH,
        'ID_MAX_LENGTH': settings.ID_MAX_LENGTH,
        'NICKNAME_MIN_LENGTH': settings.NICKNAME_MIN_LENGTH,
        'NICKNAME_MAX_LENGTH': settings.NICKNAME_MAX_LENGTH,
        'PORTRAIT_SIZE_LIMIT': settings.PORTRAIT_SIZE_LIMIT,
        'ENABLE_ALARM_POLLING': settings.ENABLE_ALARM_POLLING,
        'MAX_BOOKMARKS': settings.MAX_BOOKMARKS,
        'MSG_TEXT_MAX': settings.MSG_TEXT_MAX,
        'REPLY_IMAGE_AVAILABLE': settings.REPLY_IMAGE_AVAILABLE,
        'REPLY_IMAGE_SIZE_LIMIT': settings.REPLY_IMAGE_SIZE_LIMIT,
        'REPLY_TEXT_MAX': settings.REPLY_TEXT_MAX,
        'REPLY_AUTO_RENEW_MS': settings.REPLY_AUTO_RENEW_MS,
        'COMMENT_TEXT_MAX': settings.COMMENT_TEXT_MAX,
        'USERNAME_MAX': settings.USERNAME_MAX,
        'BLOG_CATEGORY': settings.BLOG_CATEGORY,
        'ENABLE_MASTERKEY': settings.ENABLE_MASTERKEY,
        'MASTERKEY_LENGTH': settings.MASTERKEY_LENGTH,
        'ENABLE_ADSENSE': settings.ENABLE_ADSENSE,
        'SITE_INFO': settings.SITE_INFO,
        'SITE_LOGO': settings.SITE_LOGO,
        'SITE_NAME': settings.SITE_NAME,
    }
