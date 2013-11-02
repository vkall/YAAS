from django.conf.urls import patterns, include, url
from YAAS_app.views import *
from YAAS_app.api_views import *
from django.contrib.auth.views import login, logout
from rest_framework.urlpatterns import format_suffix_patterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# RESTful API URLs
urlpatterns = patterns('',
                       (r'^YAAS/api/auctions/$', api_list_auctions),
                       (r'^YAAS/api/auctions/(?P<criteria>(\w\s*)+)/$', api_search_auctions),
)

urlpatterns = format_suffix_patterns(urlpatterns)

# Application URLs
urlpatterns += patterns('',
    (r'^YAAS/$', home),
    (r'^YAAS/search/$', search),
    (r'^YAAS/create_auction/$', create_auction),
    (r'^YAAS/view_auction/(?P<id>\d+)/$', view_auction),
    (r'^YAAS/edit_auction/(?P<id>\d+)/$', edit_auction),
    (r'^YAAS/ban_auction/(?P<id>\d+)/$', ban_auction),
    (r'^YAAS/register/$', register_user),
    (r'^YAAS/edit_user/$', edit_user),
    (r'^YAAS/login/$', login, {'template_name': 'message.html',
                               'extra_context': {'message': 'Please sign in using the login form in the navigation bar.'}}),
    (r'^YAAS/logout/$', logout, {'next_page': '/YAAS/'}),
    (r'^YAAS/confirmation/$', confirmation),

    # Comment the line below to disable database fixture
    (r'^YAAS/populate_database/$', populate_database),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
