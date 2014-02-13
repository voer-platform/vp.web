# sitemaps.py
from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from vpw.vpr_api import vpr_get_categories


class VoerSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'browse', 'about-us']

    def location(self, item):
        return reverse(item)


class VoerTypeSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['1', '2']

    def location(self, obj):
        return '/browse?type=%s' % obj


class VoerLanguagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'
    def items(self):
        return ['vi', 'en']

    def location(self, obj):
        return '/browse?languages=%s' % obj


class VoerCategoriesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        #Get all categories
        return vpr_get_categories()

    def location(self, obj):
        return '/browse?categories=%s' % obj['id']