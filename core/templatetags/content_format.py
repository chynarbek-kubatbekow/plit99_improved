import re

from django import template
from django.template.defaultfilters import linebreaks
from django.utils.safestring import mark_safe


register = template.Library()

HTML_CONTENT_RE = re.compile(
    r"</?(?:p|div|section|article|h[1-6]|ul|ol|li|blockquote|br|strong|em|b|i|a|img)\b",
    re.IGNORECASE,
)


@register.filter(is_safe=True)
def render_rich_text(value):
    text = (value or "").strip()
    if not text:
        return ""

    if HTML_CONTENT_RE.search(text):
        return mark_safe(text)

    return linebreaks(text)
