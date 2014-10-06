from django.conf.urls import patterns, include, url
from views import NewsFeed, WriteArticle, EditArticle, ReadArticle, ArticleYearArchive, ArticleMonthArchive


urlpatterns = patterns('',
	url(r'^write$', WriteArticle.as_view(), name="write-article"),
	url(r'^edit/(?P<id>\d+)/$', EditArticle.as_view(), name="admin-edit-article"),
	url(r'^read/(?P<pk>\d+)/$', ReadArticle.as_view(), name="admin-read-article"),
	url(r'^archives/(?P<year>\d{4})/$', ArticleYearArchive.as_view(), name="admin-year-archives"),
	url(r'^archives/(?P<year>\d{4})/(?P<month>\d+)/$', ArticleMonthArchive.as_view(), name="admin-month-archives"),
	)