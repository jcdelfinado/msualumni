from django import forms
from django.forms import widgets
from django.contrib.auth import authenticate
from profiles.forms import AlumInfoForm, AlumGraduationForm
from profiles.models import CAMPUSES, MONTHS
#from profiles.models import Alum

class FiltersForm(forms.Form):

  first_name = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Enter First Name', 'class':'input-sm advanced'}))
  last_name = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Enter Last Name', 'class':'input-sm advanced'}))
  middle_name = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Enter Middle Name', 'class':'input-sm advanced'}))
  class_year = forms.IntegerField(required=False, label="", min_value=1963, max_value=9999, widget=forms.NumberInput(attrs={'disabled':'', 'placeholder':'Class Year', 'type':'number', 'class':'input-sm advanced'}))
  college = forms.CharField(required=False, max_length=64, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'College', 'class':'input-sm advanced'}))
  campus = forms.ChoiceField(required=False, label="", choices = CAMPUSES, widget=forms.Select(attrs={'disabled':'', 'placeholder':'Campus', 'class':'input-sm advanced', 'type':'radio'}))
  hometown_city = forms.CharField(required=False, max_length=32,  label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Hometown City/Town', 'class':'input-sm advanced'}))
  hometown_province = forms.CharField(required=False, max_length=32,  label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Hometown Province/State', 'class':'input-sm advanced'}))
  residence_city = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Residence City/Town', 'class':'input-sm advanced'}))
  residence_province = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Residence Province/State', 'class':'input-sm advanced'}))
  residence_country = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Residence Province/State', 'class':'input-sm advanced'}))
  business_city = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Business City/Town', 'class':'input-sm advanced'}))
  business_province = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Business Province/State', 'class':'input-sm advanced'}))
  business_country = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'disabled':'', 'placeholder':'Business Country', 'class':'input-sm advanced'}))
  

class SearchForm(forms.Form):
  
  #CHOICES = (('alumni_id', 'Alumni ID'), ('last_name','Last Name'), ('first_name', 'First Name'))
  query = forms.CharField(max_length=64, required=False, label="", widget=forms.TextInput(attrs={'placeholder':'Search for alumni', 'id':'search_field'}))
  #filter = forms.ChoiceField(choices=CHOICES, label="", widget=forms.Select(attrs={'type':'radio', 'selected':'alumni_id'}))
  

class AddProfileForm(forms.Form):

  first_name = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Enter First Name', 'class':'input-sm form-inline'}))
  last_name = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Enter Last Name', 'class':'input-sm'}))
  middle_name = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Enter Middle Name', 'class':'input-sm'}))
  program = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'Program', 'class':'input-sm'}))
  major = forms.CharField(max_length=64, required="False", label="", widget=forms.TextInput(attrs={'placeholder':'Major', 'class':'input-sm'}))
  college = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'College', 'class':'input-sm'}))
  campus = forms.ChoiceField(label="", choices = CAMPUSES, widget=forms.Select(attrs={'placeholder':'Campus', 'class':'input-sm', 'type':'radio'}))
  month = forms.ChoiceField(label="", choices = MONTHS,  widget=forms.Select(attrs={'placeholder':'Month', 'type':'radio', 'class':'input-sm'}))
  year = forms.IntegerField(label="", min_value=1963, max_value=9999, widget=forms.NumberInput(attrs={'placeholder':'Year', 'type':'number', 'class':'input-sm'}))
  

class LogInForm(forms.Form):
  
  
  username = forms.EmailField(max_length=64, label="", widget=forms.EmailInput(attrs={'placeholder':'Username'}))
  password = forms.CharField(max_length=32, label="", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
  
  
  def login(self, request):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    
    print username
    print password
    return user