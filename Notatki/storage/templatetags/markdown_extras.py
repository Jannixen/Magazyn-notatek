import bleach
import markdown as md
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def markdown(text):
    return md.markdown(bleach.clean(text))
