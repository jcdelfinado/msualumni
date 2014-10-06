from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, ProcessFormView, UpdateView

from alumniadmin.forms import AddProfileForm, SearchForm
from alumniadmin.models import User
from msualumni.utils.captcha import hash
from braces import views as access

from models import *
from forms import *
import sys

class ProfileDetailView(UpdateView):
  template_name = 'profiles/profile_page.html'
  context_object_name = 'alum'
  model = Alum
  slug_field= 'alumni_id'
  form_class = EditableInfoForm

  def get_object(self):
    obj = Alum.objects.prefetch_related('grad').get(alumni_id=self.kwargs['slug'])
    return obj

  def post(self, *args, **kwargs):
    print self.request.POST
    if self.request.FILES.has_key('pic'):
      form = PhotoForm(self.request.POST, self.request.FILES)
      print form
      print self.request.FILES['pic']
      if form.is_valid():
        alum = Alum.objects.get(alumni_id=self.request.POST.get('id'))
        alum.pic = self.request.FILES['pic']
        alum.save()
    return super(ProfileDetailView, self).post(self, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(ProfileDetailView, self).get_context_data(**kwargs)
    try:
      business_data = BusinessAddress.objects.select_related('alum_set').get(id=self.object.business_address_id)
      context['business'] = BusinessForm(initial={
        'business_position': business_data.position,
        'business_company' : business_data.company,
        'business_city' : business_data.city.city,
        'business_zip' : business_data.city.zip,
        'business_province' : business_data.city.province,
        'business_country' : business_data.city.country
      })
    except:
      context['business'] = BusinessForm()
    try:
        residence_data = Residence.objects.select_related().get(id=self.object.residence_id)
        context["residence"] = ResidenceForm(initial={
          'residence_street': residence_data.street,
          'residence_barangay' : residence_data.barangay,
          'residence_city' : residence_data.city.city,
          'residence_zip' : residence_data.city.zip,
          'residence_province' : residence_data.city.province,
          'residence_country' : residence_data.city.country
        })
    except:
      print sys.exc_info()[0], sys.exc_info()[1] 
      context["residence"] = ResidenceForm()
    context['photo'] = PhotoForm()
    context['form'] = EditableInfoForm(instance=self.object)
    return context

class ProfileUpdateView(access.UserPassesTestMixin, UpdateView):
  template_name = 'profiles/profile_page.html'
  form_class = EditableInfoForm
  model = Alum
  context_object_name = 'alum'
  login_url='/login'

  def test_func(self, user):
    return (user.alumni_id_id == self.kwargs['id'])

  def get_object(self):
    obj = Alum.objects.prefetch_related('grad').get(alumni_id=self.kwargs['id'])
    return obj

  def get_context_data(self, **kwargs):
    context = super(ProfileUpdateView, self).get_context_data(**kwargs)
    # alum = self.object
    # try:
    #   hometown_data = City.objects.get(id=alum.hometown_id)
    #   context['hometown'] = HometownForm(initial={
    #     'hometown_city' : hometown_data.city,
    #     'hometown_zip' : hometown_data.zip,
    #     'hometown_province' : hometown_data.province,
    #     'hometown_country' : hometown_data.country
    #   })        
    # except:
    #   context['hometown'] = HometownForm()
    # try:
    #   business_data = BusinessAddress.objects.select_related().get(id=alum.business_address_id)
    #   context['business'] = BusinessForm(initial={
    #     'business_position': business_data.position,
    #     'business_company' : business_data.company,
    #     'business_city' : business_data.city_id.city,
    #     'business_zip' : business_data.city_id.zip,
    #     'business_province' : business_data.city_id.province,
    #     'business_country' : business_data.city_id.country
    #   })
    # except:
    #   context['business'] = BusinessForm()
    # try:
    #   residence_data = Residence.objects.select_related().get(id=alum.residence_id)
    #   context['residence'] = ResidenceForm(initial={
    #     'residence_street': residence_data.street,
    #     'residence_barangay' : residence_data.barangay,
    #     'residence_city' : residence_data.city.city,
    #     'residence_zip' : residence_data.city.zip,
    #     'residence_province' : residence_data.city.province,
    #     'residence_country' : residence_data.city.country
    #   })
    # except:
    #     context['residence'] = ResidenceForm()
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

class ProfileIndex(FormMixin, ListView):

  paginate_by = 25
  template_name = 'profiles/profiles.html'
  queryset = Alum.objects.prefetch_related('grad').all()
  form_class = SearchForm
  allow_empty = True

  def get_queryset(self, **kwargs):
      if self.request.GET.has_key('filter'):
        used_filter = {str(self.request.GET.get('filter'))+'__istartswith' : self.request.GET.get('query')}
        query = Alum.objects.prefetch_related('grad').filter(**(used_filter))
        return query
      else: 
        return Alum.objects.none()

  def get_form_class(self):
    form_class = SearchForm()
    if self.request.GET.has_key('query'):
      form_class = SearchForm(self.request.GET)
    return form_class

  def get_context_data(self, **kwargs):
    context = super(ProfileIndex, self).get_context_data(**kwargs)
    form_class = self.get_form_class()
    context['form'] = form_class
    context['total_results'] = self.object_list.count()
    if context['total_results'] < 1 and self.request.GET.has_key('filter'):
      context['alerts'] = 'Your search returned no results.'
    context['previous_query'] = self.request.GET.get('query')
    #context['request_count'] = ProfileApplication.objects.all().count() if self.request.user.is_superuser else ProfileApplication.objects.filter(status='P').count()
    queries_without_page = self.request.GET.copy()
    if queries_without_page.has_key('page'):
        del queries_without_page['page']
    context['query_params'] = queries_without_page
    return context

  def form_valid(self, form, **kwargs):
    return super(ProfilesIndexView, self).form_valid(form)

  def form_invalid(self, form, **kwargs):
    return super(ProfilesIndexView, self).form_invalid(form)

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
      from msualumni.settings import EMAIL_HOST_USER
      self.object.send_email(
        subject = "MSU Alumni Profile Request",
        context = context,
        from_email = EMAIL_HOST_USER,
        templates = {'html':'emails/request.html', 'plaintext':'emails/request.txt'}
        )
    except:
      raise
    return self.success_url
  
def signup(request):
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
      
  form = SignUpForm()
  return render(request, 'portal/signup.html', {'form' : form})
