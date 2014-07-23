from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import sys
from forms import LogInForm
from profiles.models import Alum
from models import User

def _get_preserved_query(GET):
  queries_without_page = GET
  if queries_without_page.has_key('page'):
      del queries_without_page['page']
  return queries_without_page
  
#Admin indexView
@login_required(login_url='/admin/login')
def dashboard(request):
  if request.user.is_staff:
    stats = {}
    stats['alumni'] = Alum.objects.count()
    stats['non_admin'] = User.objects.filter(is_active=True).filter(is_staff=False).count()
    stats['inactive'] = User.objects.filter(is_active=False).filter(is_staff=False).count()
    stats['for_approval'] = Alum.objects.filter(approved=False).count()
    from news import views
    articles = views._article_list(7, 1)
    return render(request, 'admin/index.html', {'stats':stats, 'articles':articles})
  return redirect('/')

@login_required(login_url='/login')
def user_logout(request):
  
  logout(request)
  return redirect('/login')
  
def user_login(request):
  
  error = False
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(password=password, username=username)
    
    if user and user.is_staff:
      login(request, user)
      return redirect('/admin/dashboard')
    else:
      error = True

  login_form = LogInForm()
  return render(request, 'admin/login.html', {'form':login_form, 'error':error})


  
  
  
  
  
  
  
  
