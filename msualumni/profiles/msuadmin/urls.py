from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from views import *

urlpatterns = patterns (
    url(r'^$', ProfilesIndexView.as_view()),
    url(r'^requests$', RequestsListView.as_view()),
    url(r'^advanced', AdvancedSearch.as_view()),
    url(r'^requests/commit$', commit_approval),
    url(r'^add$', add_profile_view),
    url(r'^add_csv$', add_csv),
    url(r'^get_profile', get_profile),
    url(r'^details', profile_details),
    url(r'^save_profile_details$', save_profile_details),
    url(r'^save_name$', save_name),
    url(r'^save_hometown$', save_hometown),
    url(r'^save_residence$', save_residence),
    url(r'^save_business$', save_business),
    url(r'^login/$',
        auth_views.login,
        {'template_name':'admin/login.html',
         'redirect_field_name':'admin/dashboard'
        }),
    #url(r'^news/', include('news.urls'))
)

