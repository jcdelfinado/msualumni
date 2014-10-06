from django.conf.urls import patterns, include, url
from msuadmin import views as msu
from views import save_profile_details, profile_update, ProfileIndex, ProfileRequest, ProfileDetailView
urlpatterns = patterns ( '',
		url(r'^$', ProfileIndex.as_view(template_name="profiles/index.html"), name='client-profiles'),
		url(r'^request$', ProfileRequest.as_view()),
		url(r'^update?', profile_update),
		url(r'^save$', save_profile_details),
		url(r'^(?P<slug>\S+)$', ProfileDetailView.as_view()),
	)