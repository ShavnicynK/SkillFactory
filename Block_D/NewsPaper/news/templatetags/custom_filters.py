from datetime import datetime
from django import template


register = template.Library()

BAD_WORDS = [
    'lorem',
    'tempor',
    'incididunt',
]

@register.filter()
def censor(content: str):
    string = content.lower()
    for word in BAD_WORDS:
        if word in string:
            word_replace = word[:1] + '*' * len(word)
            string = string.replace(word, word_replace)

    return string