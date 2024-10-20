import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='make_clickable')
def make_clickable(text):
    # Expressão regular para detectar URLs
    url_pattern = re.compile(r'(https?://[^\s]+)')
    
    # Substituir URLs por links HTML
    clickable_text = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text)
    
    # Tornar o HTML seguro para ser renderizado
    return mark_safe(clickable_text)
