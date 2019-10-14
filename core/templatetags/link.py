from django import template

register = template.Library()


@register.filter(name='target_blank', is_safe=True)
def _target_blank(link):
    return link.replace('<a href=', '<a target="_blank" href=')


@register.filter(name='filenamepath')
def _filenamepath(path):
    filename = path.split('/')[-1]
    return filename


@register.filter(name='absolutepath')
def _absolutepath(content):
    newcontent = content.replace('<img src="/upload/', '<img src="http://localhost:8000/upload/')
    return newcontent
