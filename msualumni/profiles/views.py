from django.shortcuts import render
from forms import SignUpForm
from alumniadmin.forms import AddProfileForm
# Create your views here.

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
