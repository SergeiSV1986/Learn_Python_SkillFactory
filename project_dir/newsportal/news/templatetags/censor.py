# yourapp/templatetags/censor.py

from django import template
import re

register = template.Library()

# Список нецензурных слов
BAD_WORDS = ['редиска', 'плохое_слово']  # Добавьте сюда свои слова


@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor применяется только к строкам.")

    for word in BAD_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        value = pattern.sub(word[0] + '*' * (len(word) - 1), value)

    return value