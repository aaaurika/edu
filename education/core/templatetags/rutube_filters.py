import re
from django import template

register = template.Library()

@register.filter
def rutube_id(url):
    """
    Извлекает ID видео из ссылки RuTube.
    """
    match = re.search(r'/video/([a-zA-Z0-9]+)/', url)
    return match.group(1) if match else ''
