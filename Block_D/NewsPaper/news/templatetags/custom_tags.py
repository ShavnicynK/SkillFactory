from datetime import datetime
from django import template


register = template.Library()


@register.simple_tag()
def post_date(date, format_string='%b %d %Y'):
    return date.strftime(format_string)