from django.db import models
from django.core.validators import MinValueValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

CAMPUSES = (('MSU Marawi', 'MSU Marawi'),
            ('MSU Iligan (IIT)', 'MSU Iligan (IIT)'),
            ('MSU MSAT', 'MSU MSAT'), 
            ('MSU Naawan', 'MSU Naawan'), 
            ('MSU Sulu', 'MSU Sulu'), 
            ('MSU Tawi-Tawi', 'MSU Tawi-Tawi'), 
            ('MSU General Santos', 'MSU General Santos'), 
            ('MSU LNCAT', 'MSU LNCAT'), 
            ('MSU Buug', 'MSU Buug'), 
            ('MSU Maguindanao', 'MSU Maguindanao'), 
            ('MSU LNAC', 'MSU LNAC'))
STATUS = (('V', 'Verified'),
          ('A', 'Approved'),
          ('R', 'Rejected'),
          ('P', 'Pending'),)

DEGREES = (('BS', 'Bachelor of Science'),
           ('AB', 'Bachelor of Arts'),
           ('Diploma', 'Diploma'),
           ('Certificate', 'Certificate'),
           ('MA', 'Master of Arts'),
           ('MS', 'Master of Science'),
           ('D', 'Doctorate'))
#model for storing religion. we can't really be sure how many there are so we add a model for it.
class Religion(models.Model):
  
  
  name = models.CharField(max_length=54)
  
  def __unicode__(self):
    return self.name
  
  class Meta:
    db_table='religion'
    

#model for tribe. like religion, this could go from less than 30 to 100. client side should handle duplicates with ajax requests    
class Tribe(models.Model):
  
  
  name = models.CharField(max_length=32)
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    db_table='tribe'
    


class City(models.Model):


  city = models.CharField(max_length=64)
  province = models.CharField(max_length=64)
  zip = models.CharField(max_length=16)
  country = models.CharField(max_length=64,  default="Philippines")
  
  def __unicode__(self):
    return u'%s at %s' % (self.city, self.province)
  
  class Meta:
    db_table='city'
    verbose_name_plural='Cities'   
    unique_together=(('city', 'province'),)
    
    
#model for breaking down home addresses. this makes it easier to parse address information and make information discovery faster
class Residence(models.Model):

  
  street = models.CharField(max_length=32)
  barangay = models.CharField(max_length=32)
  city = models.ForeignKey(City)
  
  def __unicode__(self):
    return u'%s %s' % (self.street, self.barangay)

  class Meta:
    db_table='residence'

  
#model for breaking down current work
class BusinessAddress(models.Model):


  position = models.CharField(max_length=64, default="Unspecified")
  company = models.CharField(max_length=96, blank=True)
  city = models.ForeignKey(City)

  def __unicode__(self):
    return u'%s at %s' % (self.position, self.company)

  class Meta:
    db_table='business_address'
    verbose_name_plural='Business Addresses'
    verbose_name='Business Address'
    
#integration model for alumnus information    
class Alum(models.Model):

  
  alumni_id = models.CharField(max_length=12, primary_key=True)
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  middle_name = models.CharField(max_length=32)
  email = models.EmailField(null=True, blank=True)
  mobile = models.CharField(max_length=12, null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  gender = models.CharField(max_length=6, null=True, blank=True)
  civil_status = models.CharField(max_length=8, null=True, blank=True)
  citizenship = models.CharField(max_length=32, null=True, blank=True)
  tribe = models.ForeignKey(Tribe, null=True, blank=True)
  religion = models.ForeignKey(Religion, null=True, blank=True)
  residence = models.ForeignKey(Residence, null=True, blank=True)
  hometown = models.ForeignKey(City, null=True, blank=True)
  business_address = models.ForeignKey(BusinessAddress, null=True, blank=True)
  pic = models.ImageField(upload_to='/media/profiles/', default='/media/profiles/no-pic.png')
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now_add=True, auto_now=True)
  is_active = models.BooleanField(default=False)
  
  def __unicode__(self):
    return u'%s %s' % (self.first_name, self.last_name)
  
  def get_full_name(self):
    """
      Returns the first name and last name of the alum separated with a space
    """
    full_name = u'%s %s'(self.first_name, self.last_name)
    return full_name.strip()

  def send_email(self, subject, context, templates, from_email=None):
    if self.email:
      try:
        html = get_template(templates['html'])
        plaintext = get_template(templates['plaintext'])
      except KeyError:
        raise

      plaintext_content = plaintext.render(context)
      html_content = html.render(context)
      try:
        email = EmailMultiAlternatives(subject, plaintext_content, from_email, [self.email])
        email.attach_alternative(html_content, 'text/html')
        email.send()
      except:
        raise
    else:
      print "No email set!"

    
  class Meta:
    db_table='alum'
    verbose_name_plural='alumni'
    
class Campus(models.Model):

  
  name = models.CharField(max_length=64)
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    db_table='campus'
    verbose_name_plural='campuses'
  
class College(models.Model):

  
  name = models.CharField(max_length=64)
  campus = models.ForeignKey(Campus)
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    db_table='college'  

    
class Program(models.Model):


  name = models.CharField(max_length=64)
  
  def __unicode__(self):
    return self.name
    
  class Meta:
    db_table='program'
  
    
class Major(models.Model):


  name = models.CharField(max_length=32, default="None")
  program = models.ForeignKey(Program)
  
  def __unicode__(self):
    if self.name:
      return u'%s (%s)' % (self.program, self.name)
    else:
      return u'%s' % (self.program)

  class Meta:
    db_table='major'
    
MONTHS = (("January", "January"), ("February", "February"), ("March", "March"), ("April", "April"),
            ("May", "May"), ("June", "June"), ("July", "July"), ("August", "August"),
            ("September", "September"), ("October", "October"), ("November", "November"), ("December", "December"))
  
class Graduation(models.Model):

  
  alumni = models.ForeignKey(Alum, related_name="grad")
  program = models.ForeignKey(Program)
  college = models.ForeignKey(College, null=True)
  month = models.CharField(max_length=10, choices=MONTHS)
  year = models.PositiveIntegerField(validators=[MinValueValidator(1963)])
  
  
  class Meta:
    db_table='graduation'
    
  def __unicode__(self):
    return u'%s (%s %d)' % (self.alumni, self.month, self.year)

class ProfileApplication(models.Model):
  """docstring for Applicant"""
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  middle_name = models.CharField(max_length=32)
  email = models.EmailField(unique=True)
  mobile = models.CharField(max_length=12, null=True, blank=True)
  birthdate = models.DateField(null=True, blank=True)
  program = models.CharField(max_length=64)
  campus = models.CharField(choices=CAMPUSES, max_length=64)
  year = models.PositiveIntegerField(validators=[MinValueValidator(1963)])
  photo = models.ImageField(upload_to='/media/applications/', default='/media/profiles/no-pic.png')
  status = models.CharField(choices=STATUS, max_length=1, default='P')
  #verified_by = models.ForeignKey(adminmodels.User)

  def send_email(self, subject, context, templates, from_email=None):
    if self.email:
      try:
        html = get_template(templates['html'])
        plaintext = get_template(templates['plaintext'])
      except KeyError:
        raise

      plaintext_content = plaintext.render(context)
      html_content = html.render(context)
      try:
        email = EmailMultiAlternatives(subject, plaintext_content, from_email, [self.email])
        email.attach_alternative(html_content, 'text/html')
        email.send()
      except:
        raise
    else:
      print "No email set!"

  def __unicode__(self):
    return u'%s %s' % (self.first_name, self.last_name)

  class Meta:
    db_table = 'profile_application'