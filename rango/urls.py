from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    #url(r'^add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^hey/(?P<name>[a-zA-Z_-]+)/$', views.hey, name='name'),
)
