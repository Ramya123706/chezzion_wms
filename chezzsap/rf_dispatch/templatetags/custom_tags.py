from django import template

register = template.Library()

@register.filter
def to(value, end):
    return range(value, end)


from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

from django import template

register = template.Library()

@register.filter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False
# rf_dispatch/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
