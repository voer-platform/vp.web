from django import template
from django.db.models.query_utils import Q
from vpw.models import Material
from vpw.vpr_api import vpr_materials_by_author, vpr_get_favorite

register = template.Library()

@register.simple_tag
def get_author_stats(author, field_name):
    aid = author.user_id
    pid = author.author_id
    stats_count = ''

    if field_name == 'unpublished':
        materials = Material.objects.filter(Q(creator_id=aid) & (Q(version=None) | Q(version=0)))
        stats_count = len(materials)

    if field_name == 'published':
        published_items = vpr_materials_by_author(pid)
        stats_count = published_items['count']

    if field_name == 'favorites':
        favorites = vpr_get_favorite(pid)
        stats_count = favorites['count']

    if stats_count:
        return ' (%s)' % stats_count

    return
