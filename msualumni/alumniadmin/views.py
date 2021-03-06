from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
import sys
from forms import LogInForm
from profiles.models import Alum, ProfileApplication
from models import User

def _get_preserved_query(GET):
  queries_without_page = GET
  if queries_without_page.has_key('page'):
      del queries_without_page['page']
  return queries_without_page

class UsersListView(ListView):
  model = User
  #queryset = User.objects.select_related('user_groups__name').all()
  paginate_by = 25
  template_name = 'profiles/users.html'

class GroupsListView(ListView):
  model = Group
  paginate_by =  25
  template_name = 'admin/groups.html'

 
#Admin indexView
@login_required(login_url='/admin/login')
def dashboard(request):
  if request.user.is_staff:
    stats = {}
    stats['alumni'] = Alum.objects.count()
    stats['non_admin'] = User.objects.filter(is_active=True).filter(is_staff=False).count()
    stats['inactive'] = User.objects.filter(is_active=False).filter(is_staff=False).count()
    stats['for_approval'] = ProfileApplication.objects.exclude(status='A').exclude(status='R').count()
    from news import views as news_views
    articles = news_views._article_list(7, 1)
    from events import views as event_views
    events = event_views.EventsIndex.queryset
    return render(request, 'admin/dashboard.html', {'stats':stats, 'events':events, 'articles':articles})
  return redirect('/')