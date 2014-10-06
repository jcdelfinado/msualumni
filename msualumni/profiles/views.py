from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, UpdateView

from alumniadmin.forms import AddProfileForm, SearchForm
from alumniadmin.models import User
from msualumni.utils.captcha import hash
from msuadmin.views import generate_id, ProfilesIndexView

from models import *
from forms import *
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

class ProfileUpdateView(UpdateView):
  template_name = 'profiles/profile_update.html'
  form_class = EditableInfoForm
  model = Alum
  context_object_name = 'alum'

  def get(self, request, **kwargs):
    self.object = Alum.objects.get(alumni_id=self.request.GET.get('id'))
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    context = self.get_context_data(object=self.object, form=form)
    return self.render_to_response(context)

  def get_object(self):
    obj = Alum.objects.get(alumni_id=self.request.GET.get('id'))
    return obj

  def get_context_data(self):
    context = super(ProfileUpdateView, self).get_context_data()
    alum = self.object
    try:
      hometown_data = City.objects.get(id=alum.hometown_id)
      context['hometown'] = HometownForm(initial={
        'hometown_city' : hometown_data.city,
        'hometown_zip' : hometown_data.zip,
        'hometown_province' : hometown_data.province,
        'hometown_country' : hometown_data.country
      })        
    except:
      context['hometown'] = HometownForm()
    try:
      business_data = BusinessAddress.objects.select_related().get(id=alum.business_address_id)
      context['business'] = BusinessForm(initial={
        'business_position': business_data.position,
        'business_company' : business_data.company,
        'business_city' : business_data.city_id.city,
        'business_zip' : business_data.city_id.zip,
        'business_province' : business_data.city_id.province,
        'business_country' : business_data.city_id.country
      })
    except:
      context['business'] = BusinessForm()
    try:
      residence_data = Residence.objects.select_related().get(id=alum.residence_id)
      context['residence'] = ResidenceForm(initial={
        'residence_street': residence_data.street,
        'residence_barangay' : residence_data.barangay,
        'residence_city' : residence_data.city.city,
        'residence_zip' : residence_data.city.zip,
        'residence_province' : residence_data.city.province,
        'residence_country' : residence_data.city.country
      })
    except:
        context['residence'] = ResidenceForm()
    return context

def profile_update(request):
  
  if request.method == 'GET':
      id = request.GET.get('id')
      try:
        alum = Alum.objects.get(alumni_id=id)
        name = NameForm(instance=alum)
        photo = PhotoForm()
        info = EditableInfoForm(
          initial={
            'citizenship' : alum.citizenship,
            'tribe' : alum.tribe,
            'religion' : alum.religion
          })
      except:
        info = EditableInfoForm()
      try:
        hometown_data = City.objects.get(id=alum.hometown_id)
        hometown = HometownForm(initial={
          'hometown_city' : hometown_data.city,
          'hometown_zip' : hometown_data.zip,
          'hometown_province' : hometown_data.province,
          'hometown_country' : hometown_data.country
        })
        
      except:
        hometown = HometownForm()
      try:
        business_data = BusinessAddress.objects.select_related().get(id=alum.business_address_id)
        business = BusinessForm(initial={
          'business_position': business_data.position,
          'business_company' : business_data.company,
          'business_city' : business_data.city_id.city,
          'business_zip' : business_data.city_id.zip,
          'business_province' : business_data.city_id.province,
          'business_country' : business_data.city_id.country
        })
      except:
        business = BusinessForm()
      try:
        residence_data = Residence.objects.select_related().get(id=alum.residence_id)
        residence = ResidenceForm(initial={
          'residence_street': residence_data.street,
          'residence_barangay' : residence_data.barangay,
          'residence_city' : residence_data.city.city,
          'residence_zip' : residence_data.city.zip,
          'residence_province' : residence_data.city.province,
          'residence_country' : residence_data.city.country
        })
      except:
        residence = ResidenceForm()
      return render(request, 'profiles/profile_update.html', {'photo':photo, 'alum':alum, 'info':info, 'residence':residence, 'hometown':hometown, 'business':business})
  return redirect('/')

def save_profile_details(request):
  
  if request.method == 'POST':
  
    try:
      info_form_data = request.POST
      info = EditableInfoForm(info_form_data)
      alum = Alum.objects.get(alumni_id=request.POST.get('id'))
    except:
      print "errors here"
    if info.is_valid():

      alum.citizenship = info.cleaned_data['citizenship']
      try:
        tribe = Tribe.objects.get(name=info.cleaned_data['tribe'])
      except:
        tribe = Tribe.objects.create(name=info.cleaned_data['tribe'])
      alum.tribe_id = tribe.id
      try:
        religion = Religion.objects.get(name=info.cleaned_data['religion'])
      except:
        religion = Religion.objects.create(name=info.cleaned_data['religion'])
      alum.religion_id = religion.id
      alum.save()
      print "Update: Saved alumni info."
      
      #try:
      #  city = Hometown.objects.get(name=hometown_form.cleaned_data['hometown_city'])
      #except:
      #  city = Hometown.objects.create(name=hometown_form.cleaned_data['hometown_city'])
      
      return redirect("/profiles?filter=alumni_id&query="+alum.alumni_id)
    else:
      print "invalid form"
  return redirect('/')

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
