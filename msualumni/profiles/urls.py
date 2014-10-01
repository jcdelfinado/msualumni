from django.conf.urls import patterns, include, url
from msuadmin import views as msu
from views import ProfileIndex, ProfileRequest, ProfileDetailView
urlpatterns = patterns ( '',
		url(r'^$', ProfileIndex.as_view(template_name="profiles/index.html"), name='client-profiles'),
		url(r'^request$', ProfileRequest.as_view()),
		url(r'^(?P<slug>\S+)$', ProfileDetailView.as_view())
	)