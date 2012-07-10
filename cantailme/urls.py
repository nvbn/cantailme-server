from django.conf.urls import patterns, include, url
from django.contrib import admin
from jsonrpc import jsonrpc_site
from django.conf import settings
import app.rpc_views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^', include('app.urls', namespace='app')),
    url(r'^json/browse/$', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)
