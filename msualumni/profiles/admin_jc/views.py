from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from django.views.generic.list import ListView

import sys, random, string, csv
from profiles.forms import NameForm, PhotoForm, AlumInfoForm, HometownForm, BusinessForm, ResidenceForm
from alumniadmin.forms import AddProfileForm, LogInForm, SearchForm, FiltersForm
from profiles.models import Alum, Campus, College, Program, Major, Graduation, City, BusinessAddress, Residence, Tribe, Religion
from alumniadmin.models import User

 

class RequestsListView(ListView):
  queryset = Alum.objects.prefetch_related('grad').filter(status='P')
  paginate_by = 25
  template_name = 'admin/profile_requests.html'

@login_required(login_url='/admin/login')
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login')
def index(request):
  
  nomatch = False
  form = SearchForm()
  filters = FiltersForm()
  if 'query' in request.GET:
    context = RequestContext(request)
    form = SearchForm(data = request.GET)
    form.full_clean()
    query = form.cleaned_data['query']
    filter = request.GET.get('filter')
    active_only = request.GET.get('active_only')
    if query == '':
      resultset = Alum.objects.all().order_by('last_name')
    else:
      if filter == 'alumni_id':
        resultset = Alum.objects.filter(alumni_id__istartswith=query).filter(status='A').order_by('last_name')
      if filter == 'first_name':
        resultset = Alum.objects.filter(first_name__icontains=query).filter(status='A').order_by('first_name')
      if filter == 'last_name':
        resultset = Alum.objects.filter(last_name__istartswith=query).filter(status='A').order_by('last_name')
    
    if active_only == 'true':
      resultset = resultset.filter(is_active=True)
    else:
      active_only = 'false'      
    
    nomatch = True
    if len(resultset) > 0:
      nomatch = False
    resultset.prefetch_related('grad')
    
    queries_without_page = request.GET.copy()
    if queries_without_page.has_key('page'):
      del queries_without_page['page']
    if queries_without_page.has_key('active_only'):
      del queries_without_page['active_only']
    total = resultset.count
    paginator = Paginator(resultset, 50)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        resultset = paginator.page(page)
    except (InvalidPage, EmptyPage):
        resultset = paginator.page(paginator.num_pages)
    return render(request, 'admin/profiles.html', {'title': 'Alumni Profiles', 'total':total, 'active_only':active_only, 'query_params':queries_without_page, 'filters':filters, 'form':form, 'resultset':resultset, 'filter':filter, 'nomatch':nomatch})
  else:    
    return render(request, 'admin/profiles.html', {'title': 'Alumni Profiles', 'filters':filters, 'form':form})

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
            status = 'A',
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
        generate_id(year)
      
      alum = Alum(alumni_id=full_id, 
        first_name=form.cleaned_data['first_name'], 
        last_name=form.cleaned_data['last_name'], 
        middle_name=form.cleaned_data['middle_name'],
        status='A',
        is_active = False)
      alum.save()
      
      grad.save()
      return HttpResponseRedirect('/admin/profile_details?id='+full_id)
  form = AddProfileForm()
  return render(request, 'admin/add_profile.html', {'form':form})

@login_required(login_url='/login')
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login')
def advanced_search(request):

  if request.method=="GET":
    filters = FiltersForm(request.GET)
    used = []
    if filters.is_valid():
      print filters.cleaned_data
      query = Alum.objects.all()
      if filters.cleaned_data['first_name']:
        query = query.filter(first_name=filters.cleaned_data['first_name'])
        used.append(('First Name', filters.cleaned_data['first_name']))
        
      if filters.cleaned_data['last_name'] and query.count() > 0:
        query = query.filter(last_name=filters.cleaned_data['last_name'])
        used.append(('Last Name', filters.cleaned_data['last_name']))
      print query.values()  
      if filters.cleaned_data['middle_name'] and query.count() > 0:
        query = query.filter(middle_name=filters.cleaned_data['middle_name'])
        used.append(('Middle Name', filters.cleaned_data['middle_name']))
      
      if filters.cleaned_data['class_year'] and query.count() > 0:
        query = query.grad_set.filter(year=filters.cleaned_data['class_year'])
        used.append(('Class Year', filters.cleaned_data['class_year']))
        
      if query.count() > 0 and filters.cleaned_data['college'] :
        query = query.filter(college__name=filters.cleaned_data['college'])
        used.append(('College', filters.cleaned_data['college']))
        
      if query.count() > 0 and filters.cleaned_data['campus'] :
        query = query.filter(college__campus=filters.cleaned_data['campus'])
        used.append(('Campus', filters.cleaned_data['campus']))

      if query.count() > 0 and filters.cleaned_data['hometown_city'] :
        query = query.filter(alumni__hometown__city__startswith = filters.cleaned_data['hometown_city'])
        used.append(('Hometown', filters.cleaned_data['hometown_city']+', '+filters.cleaned_data['hometown_province']))
      
      if query.count() > 0 and filters.cleaned_data['hometown_province'] :
        query = query.filter(alumni__hometown__province = filters.cleaned_data['hometown_province'])
        
      if query.count() > 0 and filters.cleaned_data['residence_city'] :
        query = query.filter(alumni__residence__city__startswith = filters.cleaned_data['residence_city'])
        used.append(('Residence', filters.cleaned_data['residence_city']+', '+filters.cleaned_data['residence_province']))
      
      if query.count() > 0 and filters.cleaned_data['residence_province'] :
        query = query.filter(alumni__residence__province = filters.cleaned_data['residence_province'])
        
      if query.count() > 0 and filters.cleaned_data['residence_country'] :
        query = query.filter(alumni__residence__country = filters.cleaned_data['residence_country'])
        
      if query.count() > 0 and filters.cleaned_data['business_city'] :
        query = query.filter(alumni__business__city = filters.cleaned_data['business_city'])

        
      if query.count() > 0 and filters.cleaned_data['business_province'] :
        query = query.filter(alumni__business__province = filters.cleaned_data['business_province'])
        
      if query.count() > 0 and filters.cleaned_data['business_country'] :
        query = query.filter(alumni__business__country = filters.cleaned_data['business_country'])
      
      if query.count() > 0:
        nomatch = False        
      else: 
        nomatch = True
      form = SearchForm()  
      title ='Advanced Search'
      return render(request, 'admin/profiles.html', {'title': title, 'used':used, 'form':form, 'filters':filters, 'resultset' : query, 'nomatch':nomatch})
    return redirect('/admin')

@login_required(login_url='/login')
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login')    
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
      return render(request, 'admin/profile_details.html', {'photo':photo, 'name':name, 'alum':alum, 'info':info, 'residence':residence, 'hometown':hometown, 'business':business})
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
    
      "d valid form"
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
  
  
