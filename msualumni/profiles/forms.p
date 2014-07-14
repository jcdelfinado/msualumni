


class AlumInfoForm(forms.Form):
  

  first_name = forms.CharField(max_length=32, label="First Name", widget=forms.TextInput(attrs={'placeholder':'Enter First Name'}))
  last_name = forms.CharField(max_length=32, label="Last Name", widget=forms.TextInput(attrs={'placeholder':'Enter Last Name'}))
  middle_name = forms.CharField(max_length=32, label="Middle Name", widget=forms.TextInput(attrs={'placeholder':'Enter Middle Name'}))
  birthdate = forms.DateField(label="Birth Date", widget=forms.DateInput(attrs={'type':'date'}))
  gender = forms.ChoiceField(label="Gender", choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect())
  tribe = forms.CharField(label="Tribe", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Ethnic Group'}))
  citizenship = forms.CharField(label="Nationality", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Current citizenship'}))
  religion = forms.CharField(label="Religion", max_length=32, widget=forms.TextInput(attrs={'placeholder':'Religious affiliation'}))

  
class AlumContactForm(forms.Form):


  class HomeAddress(forms.Form):
    
    
    street = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Number and Street Name'}))
    barangay = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Barangay'}))
    city = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'City/Town'}))
    zip = forms.CharField(max_length=16, label="", widget=forms.TextInput(attrs={'placeholder':'ZIP Code'}))
    province = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Province/State'}))
    country = forms.CharField(max_length=32, label="", widget=forms.TextInput(attrs={'placeholder':'Country'}))
    
    #add meta here
    
  class BusinessAddress(forms.Form):
    
    
    position = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'Position'}))
    company = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={'placeholder':'Company/Organization'}))
    city = forms.CharField(max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'City/Town'}))
    zip = forms.CharField(max_length=16,  label="", widget=forms.TextInput(attrs={'placeholder':'ZIP Code'}))
    province = forms.CharField(max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'Province/State'}))
    country = forms.CharField(max_length=32,  label="", widget=forms.TextInput(attrs={'placeholder':'Country'}))
    
    #add meta here
    
class AlumGraduationForm(forms.Form):


  program = forms.CharField(max_length=32, label="Course")
  major = forms.CharField(max_length=32, label="Major")
  college = forms.CharField(max_length=32, label="College")
  campus = forms.CharField(max_length=32, label="Campus")
  class_year = forms.Integer(min_value=1963, label="Class Year")
  
  #add meta here