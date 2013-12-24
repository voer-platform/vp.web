from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^$', 'vpw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^m/(?P<mid>[0-9a-z]+)(/(?P<version>\d+))?/?$', 'vpw.views.module_detail', name='module_detail'),
    url(r'^c/(?P<cid>[0-9a-z]+)(/(?P<mid>[0-9a-z]+))?/?$', 'vpw.views.collection_detail', name='collection_detail'),
    url(r'^browse$', 'vpw.views.browse', name='browse'),
    url(r'^signup$', 'vpw.views.signup', name='signup'),
    url(r'^about-us$', 'vpw.views.aboutus', name='about-us'),
    url(r'^create-module$', 'vpw.views.create_module', name='create_module'),
    url(r'^create-collection$', 'vpw.views.create_collection', name='create_collection'),
    url(r'^profile/(?P<pid>[0-9a-z]+)$', 'vpw.views.view_profile', name='view_profile'),
    url(r'^user/authenticate$', 'vpw.views.vpw_authenticate', name='authenticate'),
    url(r'^user/profile$', 'vpw.views.user_profile', name='user_profile'),
    url(r'^user/logout$', 'vpw.views.vpw_logout', name='logout'),
    url(r'^search/', 'vpw.views.search_result', name='search'),

    url(r'^pdf/m/(?P<mid>[0-9a-z]+)/(?P<version>\d+)/?$', 'vpw.views.get_pdf', name='get_pdf'),
    ## AJAX
    url(r'^ajax/browse$', 'vpw.views.ajax_browse', name='ajax_browse'),
    url(r'^admin/', include(admin.site.urls)),
)
