from django import template
from django.template.defaultfilters import floatformat
import math

register = template.Library()


@register.filter
def mul(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """Divide the value by the argument"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def sub(value, arg):
    """Subtract the argument from the value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def add_percentage(value, total):
    """Calculate percentage and format it"""
    try:
        if float(total) == 0:
            return "0.0%"
        percentage = (float(value) / float(total)) * 100
        return f"{percentage:.1f}%"
    except (ValueError, TypeError):
        return "0.0%"