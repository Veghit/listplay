from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()





urlpatterns = patterns('',
    url(r'^mobileT/$', 'main.myapp.views.mobileT', name='mobileT'),
    url(r'^$', 'main.myapp.views.index', name='index'),
    url(r'^index/$', 'main.myapp.views.index', name='index'),
    url(r'^mobile/$', 'main.myapp.views.mobile', name='mobile'),
    url(r'^thanks/$', 'main.myapp.views.thanks', name='thanks'),
    url(r'^main/', include('main.foo.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
