from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from msuadmin import views as msu
from views import save_profile_details, ProfileUpdateView, ProfileIndex, ProfileRequest, ProfileDetailView
urlpatterns = patterns ( '',
		url(r'^$', ProfileIndex.as_view(template_name="profiles/index.html"), name='client-profiles'),
		url(r'^(?P<slug>\d+)$', ProfileDetailView.as_view(), name="profile-page"),
		url(r'^request$', ProfileRequest.as_view()),
		url(r'^update/(?P<id>\d+)', ProfileUpdateView.as_view()),
		url(r'^save$', save_profile_details),
		url(r'^request/success$', TemplateView.as_view(template_name="portal/application_success.html")),
	)