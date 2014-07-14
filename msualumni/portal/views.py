from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect

from profiles.forms import SignUpForm
from profiles.models import Alum
from alumniadmin.models import User

import sys
# Create your views here.
def index(request):
  
  return render(request, './portal/index.html')
  

def send_activation(alum, user):

  plaintext = get_template('email.txt')
  html = get_template('email.html')
  params = Context({
    'activation_code' : user.activation_code,
    'user' : alum
    })
  text_content = plaintext.render(params)
  html_content = html.render(params)
  subject = "MSU Alumni Profile Activation"
  from_email = "jerico.delfinado@gmail.com"
  to = user.email
  
  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  msg.attach_alternative(html_content, "text/html")
  msg.send()
  
def register(request):

  form = SignUpForm()
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      id = form.cleaned_data['alumni_id']      
      try:
        alum = Alum.objects.get(alumni_id = id)
        user = User.objects.create_inactive_user(
          alumni_id = alum,
          email = form.cleaned_data['email'],
          password = form.cleaned_data['password']
          )
        send_activation(alum, user)
        return render(request, 'portal/email_sent.html')
      except IntegrityError:
        errors = "That email address is already in use."
        return render(request, 'portal/signup.html', {'form':form, 'errors':errors})
      except:
        print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
        if User.objects.get(alumni_id=id).exists():
          User.objects.get(alumni_id=id).delete()
        return render(request, 'portal/signup.html', {'form':form})
  return render(request, 'portal/signup.html', {'form':form})  
  
@csrf_protect 
def activate(request):
  if request.method == 'POST':
    print "post"
    context = RequestContext(request)
    if 'id' in request.POST:
      id = request.POST.get('id')
      print id
      try:
        user = User.objects.get(alumni_id_id=id)
        set_active(user, True)
        return HttpResponse('Active', context)
      except:
        print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
        return HttpResponse('No user account', context, status=200,)
  if request.method == 'GET':
    if 'code' in request.GET:
      code = request.GET.get('code')
    try:
      user = User.objects.get(activation_code=code)
      set_active(user, True)
      return render(request, 'portal/activation_success.html')
    except:
      print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
      return render(request, 'portal/activation_failed.html')
  
      
      
        
def set_active(user, active):
  try:
    alum = Alum.objects.get(alumni_id=user.alumni_id_id)
    print alum
    user.is_active = active
    alum.is_active = active
    user.save()
    alum.save()
    return
  except:
    print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
    
      
      
      
      
      
      
      
      
      
      
    