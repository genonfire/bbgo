from django import template

register = template.Library()


@register.inclusion_tag('menu_main.html', takes_context=True)
def menu_main(context):
    """Main navigation menu"""
    user = context['request'].user
    logo = context['SITE_LOGO']
    info = context['SITE_INFO']

    return {
        'user': user,
        'SITE_LOGO': logo,
        'SITE_INFO': info,
    }


@register.inclusion_tag('menu_sub.html')
def menu_sub():
    """Sub navigation menu"""
    return {}


@register.inclusion_tag('menu_footer.html', takes_context=True)
def menu_footer(context):
    """Footer navigation menu"""
    admin_email = context['ADMIN_EMAIL']
    return {
        'ADMIN_EMAIL': admin_email,
    }
