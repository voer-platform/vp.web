from django import template
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.template.defaultfilters import stringfilter
from vpw.models import Material
from vpw.utils import image_exists
from vpw.vpr_api import vpr_materials_by_author, vpr_get_favorite, vpr_get_person

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


@register.filter
@stringfilter
def break_keywords(value):
    """ Replace CR-LF in string value by comma character """
    return ', '.join(value.split('\n'))


@register.filter
@stringfilter
def strip(value):
    """ Replace CR-LF in string value by comma character """
    return value.strip()


@register.filter
@stringfilter
def get_unpublished_count(uid):
    materials = Material.objects.filter(Q(creator_id=uid))
    stats_count = len(materials)

    if stats_count is None:
        stats_count = 0

    return ' (%s)' % stats_count


@register.filter
@stringfilter
def get_published_count(pid):
    published_items = vpr_materials_by_author(pid)
    stats_count = published_items['count']

    if stats_count is None:
        stats_count = 0

    return ' (%s)' % stats_count


@register.filter
@stringfilter
def get_favorites_count(pid):
    favorites = vpr_get_favorite(pid)
    stats_count = favorites['count']

    if stats_count is None:
        stats_count = 0

    return ' (%s)' % stats_count


@register.filter
@stringfilter
def get_author_avatar(pid):
    author = vpr_get_person(pid)
    is_image_exists = image_exists('', reverse('get_avatar', kwargs={'pid': 1322}))

    if is_image_exists:
        return author['avatar']

    return ''
