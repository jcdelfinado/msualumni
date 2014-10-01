from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin

from alumniadmin.forms import AddProfileForm, SearchForm
from alumniadmin.models import User
from msualumni.utils.captcha import hash
from msuadmin.views import generate_id, ProfilesIndexView

from models import Alum, Graduation, Campus, Program, ProfileApplication
from forms import SignUpForm, ProfileRequestForm
import sys

class ProfileDetailView(FormMixin, DetailView):
  template_name = 'profiles/profile_page.html'
  context_object_name = 'profile'
  model = Alum
  slug_field= 'alumni_id'
  form_class = SearchForm

  def get_context_data(self, **kwargs):
    context = super(ProfileDetailView, self).get_context_data(**kwargs)
    form_class = self.get_form_class()
    context['form'] = form_class
    return context

  def get_form_class(self):
    form_class = SearchForm()
    if self.request.GET.has_key('query'):
      form_class = SearchForm(self.request.GET)
    return form_class

class ProfileIndex(ProfilesIndexView):
  def get_queryset(self, **kwargs):
      if self.request.GET.has_key('filter'):
        used_filter = {str(self.request.GET.get('filter'))+'__istartswith' : self.request.GET.get('query')}
        query = Alum.objects.prefetch_related('grad').filter(**(used_filter))
        return query
      else: 
        return Alum.objects.none()

class ProfileRequest(CreateView):
  template_name = 'registration/profile_request_form.html'
  model = ProfileApplication
  form_class = ProfileRequestForm
  success_url = '/profiles/request/success'
  captcha_error = False
  

  def form_valid(self, form):
    if int(hash(self.request.POST['captcha'])) == int(self.request.POST['captchaHash']):
      return super(ProfileRequest, self).form_valid(form)
    self.captcha_error = True
    return self.form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super(ProfileRequest, self).get_context_data(**kwargs)
    if self.captcha_error:
      context['errors'] = ["That's not the right code!"]
    return context

  def get_success_url(self):
    print self.object.id
    context = Context({'applicant' : self.object})
    try:
      self.object.send_email(
        subject = "MSU Alumni Profile Request",
        context = context,
        from_email = 'jerico.delfinado@gmail.com',
        templates = {'html':'email_request.html', 'plaintext':'email_request.txt'}
        )
    except:
      raise
    return self.success_url
  
def send_email(alum, grad, email):

  plaintext = get_template('email_request.txt')
  html = get_template('email_request.html')
  params = Context({
    'alum' : alum,
    'grad' : grad
    })
  text_content = plaintext.render(params)
  html_content = html.render(params)
  subject = "MSU Alumni Profile Request"
  from_email = "jerico.delfinado@gmail.com"
  to = email
  
  msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
  msg.attach_alternative(html_content, "text/html")
  msg.send()

def signup(request):
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
      
  form = SignUpForm()
  return render(request, 'portal/signup.html', {'form' : form})
