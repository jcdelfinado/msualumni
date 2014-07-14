from django.db import models

# Create your models here.
class Application(models.Model):

  alumni_id = models.CharField(max_length=12)
  email = models.EmailField()
  password = models.CharField(max_length=32)
  verification_code = models.CharField(max_length=16)
  date_submitted = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=1, choices=(("A","Approved"), ("R", "Rejected")))
  
  def __unicode__(self):
    return u'%s, %s - %s' % (self.alumni_id, self.email, self.status)
  
  class Meta:
    db_table='application'