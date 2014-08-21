from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import ArticleForm
from models import Article
from django.views.generic.detail import DetailView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView, YearArchiveView
from django.views.generic.edit import CreateView, UpdateView
import sys

class NewsFeed(ArchiveIndexView):
	model = Article
	allow_empty = True
	date_field = 'pub_date'
	template_name = 'news/index.html'

	def get_context_data(self, **kwargs):
		context = super(NewsFeed, self).get_context_data(**kwargs)
		context['years'] = []
		dates = Article.objects.all().datetimes('pub_date', 'year')
		for years in dates:
			context['years'].append(years.year)
		return context

class ReadArticle(DetailView):
	model = Article
	template_name = "news/read_article.html"

	def get_context_data(self, **kwargs):
		context = super(ReadArticle, self).get_context_data(**kwargs)
		context['years'] = []
		dates = Article.objects.datetimes('pub_date', 'year')
		for years in dates:
			context['years'].append(years.year)
		return context

class WriteArticle(CreateView):
	form_class = ArticleForm
	template_name = 'news/add_article.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(WriteArticle, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(NewsFeed, self).get_context_data(**kwargs)
		context['years'] = []
		dates = Article.objects.all().datetimes('pub_date', 'year')
		for years in dates:
			context['years'].append(years.year)
		return context

class EditArticle(UpdateView):
	form_class = ArticleForm
	template_name = 'news/add_article.html'

	def get(self, request, **kwargs):
		self.object = Article.objects.get(id=self.kwargs['id'])
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(object=self.object, form=form)
		return self.render_to_response(context)

	def get_object(self, queryset=None):
	    obj = Article.objects.get(id=self.kwargs['id'])
	    return obj

	def get_success_url(self, **kwargs):
		from django.core.urlresolvers import resolve
		current_url = resolve(self.request.path_info).url_name
		base_url = '/news/read/'
		if current_url == 'admin-edit-article':
			base_url = '/admin' + base_url
		return base_url + str(self.object.id)

	def get_context_data(self, **kwargs):
		context = super(NewsFeed, self).get_context_data(**kwargs)
		context['years'] = []
		dates = Article.objects.all().datetimes('pub_date', 'year')
		for years in dates:
			context['years'].append(years.year)
		return context

class ArticleYearArchive(YearArchiveView):
    queryset = Article.objects.all().only('title', 'pub_date')
    date_field = "pub_date"
    make_object_list = True
    allow_future = False

class ArticleMonthArchive(MonthArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = False

# def _article_form(*args):
# 	if args:
# 		try:
# 			article = Article.objects.get(id=args[0])
# 			form = ArticleForm(instance = article)
# 		except:
# 			print sys.exc_info()[0], sys.exc_info()[1]
# 			return None
# 	else:
# 		form = ArticleForm()
# 	return form

# def _add_article(POST, user):
# 	article_form = ArticleForm(POST)	
# 	#print article_form.author
# 	article = article_form.save(commit=False)
# 	article.author = user
# 	try:
# 		article.save()
# 		return True
# 	except:
# 		print sys.exc_info()[0], sys.exc_info()[1]
# 		return False
# def _edit_article(request, *args):
# 	article_form = ArticleForm(request.POST).save(commit=False)
# 	try:
# 		article = Article.objects.get(id=args[0])
# 	except:
# 		pass
# 	article.title = article_form.title
# 	article.content = article_form.content
# 	try:
# 		article.save()
# 		return True
# 	except:
# 		print sys.exc_info()[0], sys.exc_info()[1]
# 		return False

def _article_list(paginate_by, page_num):
	articles = Article.objects.all().order_by('-pub_date', 'title')
	paginator = Paginator(articles, paginate_by)

	try:
		page = page_num
	except ValueError:
		page = 1
	try:
		articles = paginator.page(page)
	except (InvalidPage, EmptyPage):
		articles = paginator.page(paginator.num_pages)

	return articles