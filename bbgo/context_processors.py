from django.conf import settings

def global_settings(request):
    return {
        'BOARD_LIST_COUNT': settings.BOARD_LIST_COUNT,
    }
