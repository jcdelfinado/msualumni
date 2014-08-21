from django.conf.urls import patterns, include, url
from django.contrib import admin as dj_admin
from django.contrib.auth import views as auth_views

from portal.views import index
from profiles.views import register, signup
from msualumni import settings
from msualumni.utils import captcha

dj_admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include('alumniadmin.urls')),
    url(r'^django/', include(dj_admin.site.urls)),
    url(r'^news/', include('news.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^accounts/', include('portal.urls')),
    url(r'^login/$',
        auth_views.login,
        {'template_name':'portal/login.html',
         'redirect_field_name':'/admin/dashboard'
        }),
    url(r'^signup$', signup),
    url(r'^logout$', auth_views.logout, {'next_page':'/login'}),
    url(r'^$', index),
    #url(r'^captcha/get_salt', captcha.get_salt),
)

urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
