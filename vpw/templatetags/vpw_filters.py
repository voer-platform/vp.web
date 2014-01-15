from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def normalize_string(value):
    """
    Converts to lowercase, removes non-word characters but still keep alphanumerics
    and converts spaces to hyphens. Also strips leading and trailing whitespace.
    Also converts vietnamese characters.
    """
    from vpw.utils import normalize_string
    return normalize_string(value)
