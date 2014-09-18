from django.conf.urls import patterns, include, url
from msuadmin import views as msu
from views import profile_request, ProfileRequestView
urlpatterns = patterns ( '',
		url(r'^$', msu.ProfilesIndexView.as_view(template_name="profiles/index.html"), name='client-profiles'),
		url(r'^request$', ProfileRequestView.as_view()),
	)