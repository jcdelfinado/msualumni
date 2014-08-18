from django.shortcuts import render
from forms import SignUpForm, ProfileRequestForm
from alumniadmin.forms import AddProfileForm
# Create your views here.

def profile_request(request):

	if request.method == 'POST':
		form = ProfileRequestForm(request.POST)
	form = ProfileRequestForm()
	return render(request, 'registration/profile_request_form.html', {'form':form})

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
