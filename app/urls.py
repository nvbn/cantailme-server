from django.conf.urls import patterns, url


urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    url("^tail/(?P<hash>.*)/$", "tail", name="tail"),
)
