from django import template

register = template.Library()


@register.inclusion_tag('menu_main.html', takes_context=True)
def menu_main(context):
    """Main navigation menu"""
    user = context['request'].user

    return {
        'user': user
    }


@register.inclusion_tag('menu_sub.html')
def menu_sub():
    """Sub navigation menu"""
    return {}
