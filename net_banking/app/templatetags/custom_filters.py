from django import template

register = template.Library()

@register.filter
def split_card_number(value):
    value = str(value)
    chunks = [value[i:i+4] for i in range(0, len(value), 4)]
    return chunks