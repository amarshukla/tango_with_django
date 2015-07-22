from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    #url(r'^add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^hey/(?P<name>[a-zA-Z_-]+)/$', views.hey, name='name'),
    url(r'^register/$', views.register, name='register'),
    url(r'^listUsers/$', views.listUsers),
    url(r'^userDetail/$', views.userDetail),
)

urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
