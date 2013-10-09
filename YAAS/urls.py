from django.conf.urls import patterns, include, url
from YAAS_app.views import *
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
    (r'^YAAS/login/$', login_user),
    (r'^YAAS/logout/$', logout_user),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
