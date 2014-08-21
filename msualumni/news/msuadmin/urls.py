from django.conf.urls import patterns, include, url
from news.views import NewsFeed, WriteArticle, EditArticle, ReadArticle


urlpatterns = patterns('',
	url(r'^write$', WriteArticle.as_view(success_url = '/admin/news/'), name="write-article"),
	url(r'^edit/(?P<id>\d+)/$', EditArticle.as_view(template_name="news/admin/article_update_form.html"), name="admin-edit-article"),
	url(r'^read/(?P<pk>\d+)/$', ReadArticle.as_view(template_name="news/admin/read_article.html"), name="admin-read-article")
	)