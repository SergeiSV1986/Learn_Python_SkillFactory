from django import template
import re

register = template.Library()

CENSORED_WORDS = ['редиска', 'нехороший', 'ругательство']  # список запрещённых слов

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строкам")

    def censor_word(word):
        for bad_word in CENSORED_WORDS:
            pattern = re.compile(rf'\b{bad_word[0]}{bad_word[1:].lower()}\b', re.IGNORECASE)
            word = pattern.sub(bad_word[0] + '*' * (len(bad_word) - 1), word)
        return word

    return ' '.join(censor_word(word) for word in value.split())
