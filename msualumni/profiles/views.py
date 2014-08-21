from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse
from forms import SignUpForm, ProfileRequestForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from alumniadmin.forms import AddProfileForm
from models import Alum, Graduation, Campus, Program
from msualumni.utils.captcha import hash
from admin_jc.views import generate_id
import sys
# Create your views here.

def profile_request(request):
  messages = []
  errors = []

  form = ProfileRequestForm()
  if request.method == 'POST':
    print 'POST'
    print hash(request.POST['captcha'])
    print request.POST['captchaHash']
    print hash(request.POST['captcha']) == request.POST['captchaHash']
    form = ProfileRequestForm(request.POST)  
    if int(hash(request.POST['captcha'])) == int(request.POST['captchaHash']):
         
      print form.is_valid()
      print form.cleaned_data
      year = form.cleaned_data['year'].year
      full_id = generate_id(year)
      while Alum.objects.filter(alumni_id=full_id).exists():
        full_id = generate_id(year)

      alum = Alum(alumni_id=full_id, 
        first_name=form.cleaned_data['first_name'], 
        last_name=form.cleaned_data['last_name'], 
        middle_name=form.cleaned_data['middle_name'],
        status='P',
        is_active = False)
      alum.save()
      
      #campus, created = Campus.objects.get_or_create(name=form.cleaned_data['campus'])
      
      program, created = Program.objects.get_or_create(name=form.cleaned_data['program'])
      grad = Graduation(
          alumni_id = alum.alumni_id,
          program_id = program.id,
          year = year,
          month = form.cleaned_data['year'].month
      )
      grad.save()
      try:
        send_email(alum, grad, form.cleaned_data['email'])
      except:
        print sys.exc_info()[0], sys.exc_info()[1]
      #print "Your request was successfully sent. An email was also sent to <strong>"+ form.cleaned_data['email'] +"</strong> for your reference."
      messages.append("Your request was successfully sent. An email was also sent to "+ form.cleaned_data['email'] +" for your reference.")
      #return render_to_response("success_alert.html", {'msg' : msg}, context)
    else:      
      errors.append("That's not the right code!")
      #return render_to_response("error_alert.html", {'msg' : msg}, context)
  
  
  return render(request, 'registration/profile_request_form.html', {'form':form, 'messages':messages, 'errors':errors})

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


def register(request):
  
  if request.method == 'POST':
    form = AddProfileForm(request.POST)
      
  form = AddProfileForm()
  return render(request, 'portal/register.html', {'form' : form})
  
def signup(request):
  
  if request.method == 'POST':
    form = SignUpForm(request.POST)
      
  form = SignUpForm()
  return render(request, 'portal/signup.html', {'form' : form})
