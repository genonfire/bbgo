from django import template

register = template.Library()


@register.inclusion_tag('blogs/show_tags.html', takes_context=True)
def show_tags(context, tags):
    """Show tags"""
    splits = tags.split(',')
    for index, tag in enumerate(splits):
        splits[index] = tag.lstrip()

    return {
        'tags': splits,
    }
