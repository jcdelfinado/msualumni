from django.db import models
from alumniadmin.models import User


# Create your models here.
class Event(models.Model):
  
  title = models.CharField(max_length=64)
  details = models.CharField(max_length=160)
  date = models.DateField()
  author = models.ForeignKey(User, related_name='author')
  guests = models.ManyToManyField(User)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)