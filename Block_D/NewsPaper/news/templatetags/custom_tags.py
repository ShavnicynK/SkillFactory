from datetime import datetime
from django import template


register = template.Library()


@register.simple_tag()
def some_tag():
    return