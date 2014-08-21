from django.conf.urls import patterns, include, url
from views import NewsFeed, WriteArticle, ReadArticle


urlpatterns = patterns('',
	url(r'^write$', WriteArticle.as_view(), name="write-article"),
	url(r'^read/(?P<pk>\d+)/$', ReadArticle.as_view(template_name="news/read_article.html"), name="read-article"),
	url(r'^$', NewsFeed.as_view(), name="news-feed")
	)