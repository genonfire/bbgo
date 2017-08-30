from django import template

register = template.Library()


@register.inclusion_tag('show_navigator.html', takes_context=True)
def show_navigator(context):
    """Show navigator"""
    table = context['table']
    page = context['page']
    index_begin = context['index_begin']
    index_end = context['index_end']
    index_total = context['index_total']
    mindex_begin = context['mindex_begin']
    mindex_end = context['mindex_end']
    writable = context['writable']

    return {
        'table': table,
        'page': page,
        'index_begin': index_begin,
        'index_end': index_end,
        'index_total': index_total,
        'mindex_begin': mindex_begin,
        'mindex_end': mindex_end,
        'writable': writable,
    }
