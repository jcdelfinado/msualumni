from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from forms import ArticleForm
from models import Article
import sys

def index(request):

	articles = _article_list(5, 1)

	return render(request, 'news/index.html', {'articles':articles})

def _article_form(*args):
	if args:
		try:
			article = Article.objects.get(id=args[0])
			form = ArticleForm(instance = article)
		except:
			print sys.exc_info()[0], sys.exc_info()[1]
			return None
	else:
		form = ArticleForm()
	return form

def _add_article(POST, user):
	article_form = ArticleForm(POST)	
	#print article_form.author
	article = article_form.save(commit=False)
	article.author = user
	try:
		article.save()
		return True
	except:
		print sys.exc_info()[0], sys.exc_info()[1]
		return False
def _edit_article(request, *args):
	article_form = ArticleForm(request.POST).save(commit=False)
	try:
		article = Article.objects.get(id=args[0])
	except:
		pass
	article.title = article_form.title
	article.content = article_form.content
	try:
		article.save()
		return True
	except:
		print sys.exc_info()[0], sys.exc_info()[1]
		return False

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