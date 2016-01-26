from django import template

register = template.Library()


@register.filter(name='divide')
def divide(value, arg): return round(int(value) / int(arg), 1)