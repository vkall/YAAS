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
    (r'^YAAS/auction/create/$', create_auction),
    (r'^YAAS/auction/create/confirmation/$', confirmation),
    (r'^YAAS/auction/search/$', search),
    (r'^YAAS/language/$', change_language),
    (r'^YAAS/auction/(?P<id>\d+)/$', view_auction),
    (r'^YAAS/auction/(?P<id>\d+)/edit/$', edit_auction),
    (r'^YAAS/auction/(?P<id>\d+)/bid/$', bid_auction),
    (r'^YAAS/auction/(?P<id>\d+)/ban/$', ban_auction),
    (r'^YAAS/user/register/$', register_user),
    (r'^YAAS/user/$', edit_user),
    (r'^YAAS/login/$', login, {'template_name': 'message.html',
                               'extra_context': {'message': 'Please sign in using the login form in the navigation bar.'}}),
    (r'^YAAS/logout/$', logout, {'next_page': '/YAAS/'}),

    # Comment the line below to disable database fixture
    (r'^YAAS/populate_database/$', populate_database),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
