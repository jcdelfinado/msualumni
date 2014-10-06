from django import forms
from django.forms import widgets
from models import CAMPUSES, MONTHS
from models import Alum, ProfileApplication

class SignUpForm(forms.Form):

  alumni_id = forms.CharField(max_length=32, label="Alumni ID", widget=forms.TextInput(attrs={'placeholder':'Valid Alumni ID'}))
  email = forms.EmailField(max_length=64, label="Email Address", widget=forms.EmailInput(attrs={'placeholder':'Valid Email Address'}))
  password = forms.CharField(max_length=32, min_length=8, label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
  confirm_password = forms.CharField(max_length=32, label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder':'Password (again)'}))


class PhotoForm(forms.Form):

  photo = forms.ImageField(label="", required=False, widget=forms.FileInput(attrs={'class':'btn btn-default'}))

class NameForm(forms.ModelForm):

  class Meta:
    model = Alum
    fields = ['first_name', 'middle_name', 'last_name']

class EditableInfoForm(forms.Form):

  tribe = forms.CharField(required=True, label="Tribe", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Ethnic Group'}))
  citizenship = forms.CharField(required=True, label="Nationality", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Current citizenship'}))
  religion = forms.CharField(required=True, label="Religion", max_length=54, widget=forms.TextInput(attrs={'placeholder':'Religious affiliation'}))

class AlumInfoForm(forms.Form):

  birthdate = forms.DateField(required=False, label="Birth Date", widget=forms.DateInput(attrs={'type':'date', 'max':'2000-01-01'}))
  gender = forms.ChoiceField(required=True, label="Gender", choices=(("Male", "Male"), ("Female", "Female")))
  tribe = forms.CharField(required=True, label="Tribe", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Ethnic Group'}))
  citizenship = forms.CharField(required=True, label="Nationality", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Current citizenship'}))
  religion = forms.CharField(required=True, label="Religion", max_length=54, widget=forms.TextInput(attrs={'placeholder':'Religious affiliation'}))
  email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder':'Email Address'}))
  

  #residence
class ResidenceForm(forms.Form):
  residence_street = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Number and Street Name', 'class':'input-sm'}))
  residence_barangay = forms.CharField(required=False, max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Barangay', 'class':'input-sm'}))
  residence_city = forms.CharField(required=True, max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'City/Town', 'class':'input-sm'}))
  residence_zip = forms.CharField(required=True, max_length=16, label="", widget=forms.TextInput(attrs={'placeholder':'ZIP Code', 'class':'input-sm'}))
  residence_province = forms.CharField(required=True, max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Province/State', 'class':'input-sm'}))
  residence_country = forms.CharField(required=True, max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Country', 'class':'input-sm'}))
  
class BusinessForm(forms.Form):   
  business_position = forms.CharField(required=False, max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'Position', 'class':'input-sm'}))
  business_company = forms.CharField(required=False, max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'Company/Organization', 'class':'input-sm'}))
  business_city = forms.CharField(required=False, max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'City/Town', 'class':'input-sm'}))
  business_zip = forms.CharField(required=False, max_length=16,  label="", widget=forms.TextInput(attrs={'placeholder':'ZIP Code', 'class':'input-sm'}))
  business_province = forms.CharField(required=False, max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'Province/State', 'class':'input-sm'}))
  business_country = forms.CharField(required=False, max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'Country', 'class':'input-sm'}))
  
class HometownForm(forms.Form):
  hometown_city = forms.CharField(required=True, max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'City/Town', 'class':'input-sm'}))
  hometown_zip = forms.CharField(required=True, max_length=16,  label="", widget=forms.TextInput(attrs={'placeholder':'ZIP Code', 'class':'input-sm'}))
  hometown_province = forms.CharField(required=True, max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'Province/State', 'class':'input-sm'}))
  hometown_country = forms.CharField(required=True, max_length=64,  label="", widget=forms.TextInput(attrs={'placeholder':'Country', 'class':'input-sm'}))

class ProfileUpdateForm(forms.Form):
  alum = AlumInfoForm()
  residence = ResidenceForm()
  business = BusinessForm()
  hometown = HometownForm()
    
class AlumGraduationForm(forms.Form):


  program = forms.CharField(max_length=64, label="Program", widget=forms.TextInput(attrs={'placeholder':'Program', 'class':'input-sm'}))
  # major = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'Major', 'class':'input-sm'}))
  # college = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'College', 'class':'input-sm'}))
  campus = forms.ChoiceField(label="Campus", choices = CAMPUSES, widget=forms.Select(attrs={'placeholder':'Campus', 'class':'input-sm', 'type':'radio'}))
  year = forms.DateField(label="Date", widget=forms.DateInput(attrs={'placeholder':'Graduation Date', 'type':'month', 'class':'date input-sm'}))
  
class ProfileRequestForm(forms.ModelForm):
  captcha = forms.CharField(label="Just to prove you're human", max_length=6, widget=forms.TextInput(attrs={'id':'captcha_field', 'placeholder':"Enter the code above",}))
  captchaHash = forms.IntegerField(widget=forms.HiddenInput())

  class Meta:
    model = ProfileApplication
    exclude = ['status']