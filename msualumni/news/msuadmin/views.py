from news.views import *
from portal.access import MSUAdminMixin

from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy

class NewsFeed(MSUAdminMixin, NewsFeed):
	template_name="news/admin/index.html"

class ReadArticle(MSUAdminMixin, ReadArticle, DeleteView):
	template_name="news/admin/read_article.html"
	model = Article
	success_url = reverse_lazy('admin-news-feed')

class WriteArticle(MSUAdminMixin, WriteArticle):
	success_url = '/admin/news/'

class EditArticle(MSUAdminMixin, EditArticle, DeleteView):
	template_name="news/admin/article_update_form.html"
	model = Article
	success_url = reverse_lazy('admin-news-feed')

class ArticleYearArchive(MSUAdminMixin, ArticleYearArchive):
    template_name="news/admin/archives.html"

class ArticleMonthArchive(MSUAdminMixin, ArticleMonthArchive):
    template_name="news/admin/archives.html"
    month_format='%m'