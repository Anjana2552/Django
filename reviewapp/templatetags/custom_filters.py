from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    """Lookup a dictionary value by key in templates"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0

@register.filter
def multiply(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0