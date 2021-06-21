from django import template

register = template.Library()

@register.filter
def intstr(arg):
    return str(arg)