from html import unescape
import re

from django import template
from django.template.defaultfilters import linebreaks
from django.utils.safestring import mark_safe


register = template.Library()

GENERIC_HTML_TAG_RE = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")


def decode_html_entities(text, max_passes=5):
    decoded = text
    for _ in range(max_passes):
        next_value = unescape(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    return decoded


@register.filter(is_safe=True)
def render_rich_text(value):
    text = (value or "").strip()
    if not text:
        return ""

    decoded_text = decode_html_entities(text)
    if GENERIC_HTML_TAG_RE.search(decoded_text):
        return mark_safe(decoded_text)

    return linebreaks(decoded_text)
