from django import template

register = template.Library()


@register.filter(name='pick_first')
def _pick_first(list, index):
    return list[int(index)][0]


@register.filter(name='pick_second')
def _pick_second(list, index):
    return list[int(index)][1]


@register.filter(name='pick_third')
def _pick_third(list, index):
    return list[int(index)][2]
