from django import template

register = template.Library()


@register.filter(name='censor_ip')
def _censor_ip(ip):
    ip_list = ip.split('.')
    if len(ip_list) == 4:
        return ip_list[0] + '.' + ip_list[1] + '.*.*'
    else:
        return ip
