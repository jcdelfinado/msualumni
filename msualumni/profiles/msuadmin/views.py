from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from django.views.generic.list import ListView
from django.template import Context
from django.views.generic.edit import FormMixin, CreateView

import sys, random, string, csv

from profiles.forms import NameForm, PhotoForm, AlumInfoForm, HometownForm, BusinessForm, ResidenceForm
from alumniadmin.forms import AddProfileForm, LogInForm, SearchForm, FiltersForm
from profiles.models import Alum, Campus, College, Program, Major, Graduation, City, BusinessAddress, Residence, Tribe, Religion, ProfileApplication
from alumniadmin.models import User
from portal.access import MSUAdminMixin
from profiles.views import ProfileIndex

class RequestsListView(MSUAdminMixin, ListView):
  paginate_by = 25
  template_name = 'profiles/profile_requests.html'

  def get_queryset(self):
    queryset = ProfileApplication.objects.exclude(status='A').exclude(status='R')

    if not self.request.user.is_superuser:
      queryset = queryset.exclude(status='V')
    return queryset

def commit_approval(request):
  context = RequestContext(request)
  try:
    if request.method == 'POST':
      applicant_id = request.POST.get('applicant_id')
      action = request.POST.get('action_taken')
      applicant = ProfileApplication.objects.get(id=applicant_id)
      
      if action == 'recommend':
        applicant.status = 'V'
        applicant.save()
        msg = "Recommended"
        
      if action == 'approve':        
        id = generate_id(applicant.year)
        new_alum = Alum(alumni_id = id,
                    first_name=applicant.first_name,
                    last_name=applicant.last_name,
                    middle_name=applicant.middle_name,
                    birthdate=applicant.birthdate)
        new_alum.save()
        program, created = Program.objects.get_or_create(name=applicant.program)
        if created:
          program.save()
        new_grad = Graduation(
                    alumni_id = id,
                    program = program,
                    year = applicant.year
                    )
        new_grad.save()
        applicant.status = 'A'
        applicant.save()
        from msualumni.settings import EMAIL_HOST_USER as default
        applicant.send_email("MSU Alumni Profile Approval", Context({'alum':new_alum}), 
                            {'html':'emails/approved.html', 'plaintext':'emails/approved.txt'}, default)
        applicant.delete()
        msg = "Approved"
    return HttpResponse(msg)
  except:
    print sys.exc_info()[0], sys.exc_info()[1]
    return HttpResponse("Oops!", code=400)
  return redirect('/')

class ProfilesIndexView(MSUAdminMixin, ProfileIndex):
  
  def get_queryset(self, **kwargs):
    if self.request.GET.has_key('filter'):
      used_filter = {str(self.request.GET.get('filter'))+'__istartswith' : self.request.GET.get('query')}
      query = Alum.objects.prefetch_related('grad').filter(**(used_filter))
      return query
    else: 
      return Alum.objects.prefetch_related('grad').all()

  def get_context_data(self, **kwargs):
    context = super(ProfilesIndexView, self).get_context_data(**kwargs)
    context['request_count'] = ProfileApplication.objects.all().count() if self.request.user.is_superuser else ProfileApplication.objects.filter(status='P').count()
    return context


class AdvancedSearch(ProfilesIndexView):
  template_name = 'profiles/client_advanced_search.html'
  form_class = FiltersForm

  def get_form_class(self):
    form_class = FiltersForm()
    return form_class

  def get_queryset(self):
    used_filter = self.request.GET.dict()
    mod_filter = {}
    for key, value in used_filter.iteritems():
      mod_filter[key+'__istartswith'] = value
    queryset = Alum.objects.select_related('grad').filter(**(mod_filter))
    print queryset
    return queryset

class AddProfileView(MSUAdminMixin, CreateView):
  model = Alum
  form_class = AddProfileForm
  template_name = 'profiles/add_profile.html'

@login_required(login_url='/login')
def add_csv(request):

  csv_file = request.FILES['csv_file']
  data = csv.DictReader(csv_file, delimiter=';')
  count = 0
  for d in data:
    print d
    if not Alum.objects.filter(alumni_id=d['alumni_id']).exists():
      alum = Alum(alumni_id = d['alumni_id'], 
            first_name = d['first'],
            last_name = d['last'],
            middle_name = d['middle'],
            is_active = False)
      alum.save()
    
    campus, created = Campus.objects.get_or_create(name=d['campus'])
    #college, created = College.objects.get_or_create(name=d['college'], campus_id=campus.id)
    program, created = Program.objects.get_or_create(name=d['program'])
      
    grad = Graduation(alumni_id = d['alumni_id'],
                      program_id = program.id,
                      #college_id = college.id,
                      month = d['month'], 
                      year = int(d['year']))
    grad.save()
    count += 1
  return render(request, 'add_success.html', {'count':count})


#@login_required(login_url='/login')
#@user_passes_test(lambda u:u.is_staff, login_url='/admin/login')
def get_profile(request):

  context = RequestContext(request)
  
  id = request.GET.get('id')
  profile = Alum.objects.get(alumni_id=id)
  grads = Graduation.objects.filter(alumni_id=id)

  return render_to_response('profile_preview.html', {'profile' : profile, 'grads':grads}, context)
    

def generate_id(year):
  
  id = ''.join(random.choice(string.digits) for _ in range(4))
  return str(year) + id

  
@login_required(login_url='/login')
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login')
def add_profile_view(request):
  
  if request.method == 'POST':
    form = AddProfileForm(request.POST or None)
    if form.is_valid():
      year = form.cleaned_data['year']
      full_id = generate_id(year)
      
      while Alum.objects.filter(alumni_id=full_id).exists():
        full_id = generate_id(year)
      
      alum = Alum(alumni_id=full_id, 
        first_name=form.cleaned_data['first_name'], 
        last_name=form.cleaned_data['last_name'], 
        middle_name=form.cleaned_data['middle_name'],
        is_active = False)
      alum.save()
      campus, created = Campus.objects.get_or_create(name=form.cleaned_data['campus'])
      if created: campus.save()
      college, created = College.objects.get_or_create(name=form.cleaned_data['college'], campus_id=campus.id)
      if created: college.save()
      program, created = Program.objects.get_or_create(name=form.cleaned_data['program'])
      if created: program.save()

      grad = Graduation(alumni_id = alum.alumni_id,
                      program_id = program.id,
                      college_id = college.id,
                      month = form.cleaned_data['month'], 
                      year = int(form.cleaned_data['year']))
      grad.save()
      return HttpResponseRedirect('/admin/profiles')
  form = AddProfileForm()
  return render(request, 'profiles/add_profile.html', {'form':form})

@login_required(login_url='/login')
#@user_passes_test(lambda u:u.is_staff, login_url='/admin/login')    
def profile_details(request):
  
  if request.method == 'GET':
      id = request.GET.get('id')
      try:
        alum = Alum.objects.get(alumni_id=id)
        name = NameForm(instance=alum)
        photo = PhotoForm()
        info = AlumInfoForm(
          initial={
            'birthdate':alum.birthdate,
            'gender' : alum.gender,
            'citizenship' : alum.citizenship,
            'tribe' : alum.tribe,
            'religion' : alum.religion,
            'email':alum.email
          })
      except:
        info = AlumInfoForm()
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
      return render(request, 'profiles/profile_details.html', {'photo':photo, 'name':name, 'alum':alum, 'info':info, 'residence':residence, 'hometown':hometown, 'business':business})
  return redirect('/admin')
  
  
def save_hometown(request):
  
  if request.method == 'POST':
    
    hometown_data = QueryDict(request.POST.get('hometown'))
    hometown_form = HometownForm(hometown_data)
    alum = Alum.objects.get(alumni_id=request.POST.get('id'))
    if hometown_form.is_valid():      
      hometown, created = City.objects.get_or_create(city = hometown_form.cleaned_data['hometown_city'],
          province = hometown_form.cleaned_data['hometown_province'],
          country = hometown_form.cleaned_data['hometown_country']
        )
      hometown.zip = hometown_form.cleaned_data['hometown_zip']
      hometown.save() 
      alum.hometown_id = hometown.id
      alum.save()
      print "Update: Saved hometown."
      return HttpResponse("Hometown updated")
  return redirect("/admin/profiles")
  
def save_name(request):
  try:
    if request.method == 'POST':
      name = QueryDict(request.POST.get('name'))
      alum = Alum.objects.get(alumni_id=request.POST.get('id'))
      print alum
      name_form = NameForm(name, instance=alum)
      name_form.save()
  except:
    print sys.exc_info()[0], sys.exc_info()[1]
  return HttpResponse('sdada')

def save_business(request):

  if request.method == 'POST':
    
    business_data = QueryDict(request.POST.get('business'))
    business_form = BusinessForm(business_data)
    alum = Alum.objects.get(alumni_id=request.POST.get('id'))
    if business_form.is_valid():
      city, created = City.objects.get_or_create(
          city = business_form.cleaned_data['business_city'],
          province = business_form.cleaned_data['business_province'],
          zip = business_form.cleaned_data['business_zip'],
          country = business_form.cleaned_data['business_country']
        )
      if created:
        city.save()
      try:
        business, created = BusinessAddress.objects.get_or_create(
          position=business_form.cleaned_data['business_position'],
          company=business_form.cleaned_data['business_company'],
          city_id=city.id          
          )
      except:
        business = BusinessAddress()
        business.position = business_form.cleaned_data['business_position']
        business.company = business_form.cleaned_data['business_company']
        business.city = business_form.cleaned_data['business_city']
        business.zip = business_form.cleaned_data['business_zip']
        business.province = business_form.cleaned_data['business_province']
        business.country = business_form.cleaned_data['business_country']
        business.save() 
      alum.business_address_id = business.id
      alum.save()
      print "Update: Saved business address."
      return HttpResponse("Business address updated")
  return redirect("/admin/profiles")
  
def save_residence(request):

  if request.method == 'POST':
    
    residence_data = QueryDict(request.POST.get('residence'))
    residence_form = ResidenceForm(residence_data)
    alum = Alum.objects.get(alumni_id=request.POST.get('id'))
    if residence_form.is_valid():
      city, created = City.objects.get_or_create(
          city = residence_form.cleaned_data['residence_city'],
          province = residence_form.cleaned_data['residence_province'],
          zip = residence_form.cleaned_data['residence_zip'],
          country = residence_form.cleaned_data['residence_country']
        )
      try:
        residence, created = ResidenceAddress.objects.get_or_create(
          street=residence_form.cleaned_data['residence_street'],
          barangay=residence_form.cleaned_data['residence_barangay'],
          city_id=city.id
          )
      except:
        residence = Residence()
        residence.street = residence_form.cleaned_data['residence_street']
        residence.barangay = residence_form.cleaned_data['residence_barangay']
        residence.city_id = city.id
        residence.save()
        print sys.exc_info()[0], sys.exc_info()[1]   
      alum.residence_id = residence.id
      alum.save()
      return HttpResponse("Residence updated")
  return redirect("/admin/profiles")
  
  
def save_profile_details(request):
  
  if request.method == 'POST':
  
    try:
      info_form_data = request.POST
      info = AlumInfoForm(info_form_data)
      alum = Alum.objects.get(alumni_id=request.POST.get('id'))
    except:
      print "errors here"
    if info.is_valid():

      alum.birthdate = info.cleaned_data['birthdate']
      alum.gender = info.cleaned_data['gender']
      alum.citizenship = info.cleaned_data['citizenship']
      alum.email = info.cleaned_data['email']
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
      
      return redirect("/admin/profiles/details?id="+alum.alumni_id)
    else:
      print "invalid form"
  return index(request)
  
  
