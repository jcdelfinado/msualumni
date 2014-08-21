from django.conf.urls import patterns, include, url
from views import NewsFeed, WriteArticle, ReadArticle, ArticleYearArchive, ArticleMonthArchive


urlpatterns = patterns('',
	url(r'^write$', WriteArticle.as_view(), name="write-article"),
	url(r'^read/(?P<pk>\d+)/$', ReadArticle.as_view(template_name="news/read_article.html"), name="read-article"),
	url(r'^archives/(?P<year>\d{4})/$', ArticleYearArchive.as_view(template_name="news/archives.html"), name="year-archives"),
	url(r'^archives/(?P<year>\d{4})/(?P<month>\d+)/$', ArticleMonthArchive.as_view(template_name="news/archives.html", month_format='%m'), name="year-archives"),
	url(r'^$', NewsFeed.as_view(), name="news-feed")
	)