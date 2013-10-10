from django.conf.urls import patterns, include, url
from YAAS_app.views import *
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'YAAS.views.home', name='home'),
    # url(r'^YAAS/', include('YAAS.foo.urls')),
    (r'^YAAS/$', home),
    (r'^YAAS/create_auction/$', create_auction),
    (r'^YAAS/view_auction/(?P<id>\d+)/$', view_auction),
    (r'^YAAS/register/$', register_user),
    (r'^YAAS/login/$', login, {'template_name': 'message.html',
                               'extra_context': {'message': 'Please sign in using the login form in the navigation bar.'}}),
    (r'^YAAS/logout/$', logout, {'next_page': '/YAAS/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
