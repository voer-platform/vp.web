from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    url(r'^language/', include('django.conf.urls.i18n')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^mce_filebrowser/', include('mce_filebrowser.urls')),
    url(r'^profile/(?P<pid>[0-9a-z]+)/delete$', 'vpw.views.delete_profile', name='delete_profile'),

    url(r'^$', 'vpw.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^m/(?P<mid>[0-9a-z]+)(/(?P<version>\d+))?/?$', 'vpw.views.module_detail', name='module_detail'),
    url(r'^c/(?P<cid>[0-9a-z]+)(/(?P<mid>[0-9a-z]+))?/?$', 'vpw.views.collection_detail', name='collection_detail'),
    url(r'^browse$', 'vpw.views.browse', name='browse'),
    url(r'^signup$', 'vpw.views.signup', name='signup'),
    url(r'^about-us$', 'vpw.views.aboutus', name='about-us'),
    url(r'^profile/(?P<pid>[0-9a-z]+)$', 'vpw.views.view_profile', name='view_profile'),

    ## User ###
    url(r'^user/', include('registration.backends.default.urls')),
    url(r'^user/authenticate$', 'vpw.views.vpw_authenticate', name='authenticate'),
    url(r'^user/dashboard/?$', 'vpw.views.user_dashboard', name='user_dashboard'),
    url(r'^user/logout$', 'vpw.views.vpw_logout', name='logout'),
    url(r'^user/create/module/?$', 'vpw.views.create_module', name='create_module'),
    url(r'^user/create/collection/?$', 'vpw.views.create_collection', name='create_collection'),
    url(r'^user/edit/profile/?$', 'vpw.views.edit_profile', name='edit_profile'),
    url(r'^user/m/(?P<mid>[0-9]+)/?$', 'vpw.views.user_module_detail', name='user_module_detail'),
    url(r'^user/c/(?P<cid>[0-9a-z]+)(/(?P<mid>[0-9a-z]+))?/?$', 'vpw.views.user_collection_detail',
        name='user_collection_detail'),
    url(r'^user/most-viewed/?$', 'vpw.views.mostViewedView', name='most-viewed'),


    url(r'^search/', 'vpw.views.search_result', name='search'),

    url(r'^pdf/m/(?P<mid>[0-9a-z]+)/(?P<version>\d+)/?$', 'vpw.views.get_pdf', name='get_pdf'),
    url(r'^attachment/m/(?P<fid>[0-9a-z]+)/?$', 'vpw.views.get_attachment', name='get_attachment'),

    ## AJAX
    url(r'^ajax/browse$', 'vpw.views.ajax_browse', name='ajax_browse'),
    url(r'^ajax/add_favorite$', 'vpw.views.ajax_add_favorite', name='ajax_add_favorite'),
    url(r'^ajax/search_author$', 'vpw.views.ajax_search_author', name='ajax_search_author'),
    url(r'^ajax/search_module$', 'vpw.views.ajax_search_module', name='ajax_search_module'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='frontend/robots.txt', content_type='text/plain')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
