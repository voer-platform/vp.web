from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'vpw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^m/(?P<mid>[0-9a-z]+)(/(?P<version>\d+))?/?$', 'vpw.views.module_detail', name='material_detail'),
    url(r'^browse$', 'vpw.views.browse'),
    url(r'^signup$', 'vpw.views.signup'),
    url(r'^about-us$', 'vpw.views.aboutus'),
    url(r'^create-module$', 'vpw.views.create_module', name='create_module'),
    url(r'^create-collection$', 'vpw.views.create_collection', name='create_collection'),
    url(r'^profile/(?P<pid>[0-9a-z]+)$', 'vpw.views.view_profile', name='view_profile'),
    url(r'^admin/', include(admin.site.urls)),
)
