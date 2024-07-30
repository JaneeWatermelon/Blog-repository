from django import template

register = template.Library()

@register.filter
def my_int(value):
    if value >= 1000000000:
        return f'{round(value/1000000000, 1)} b'
    elif value >= 1000000:
        return f'{round(value / 1000000, 1)} m'
    elif value >= 1000:
        return f'{round(value / 1000, 1)} t'
    else:
        return value
