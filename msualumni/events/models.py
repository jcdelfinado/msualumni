from django.db import models
from alumniadmin.models import User


# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=256)

	def __unicode__(self):
		return self.name

class Event(models.Model):
  
  title = models.CharField(max_length=64)
  description = models.CharField(max_length=160)
  venue = models.CharField(max_length=140)
  date = models.DateField()
  time = models.TimeField(null=True, blank=True)
  is_private = models.BooleanField(default=False)
  is_approved = models.BooleanField(default=False)
  author = models.ForeignKey(User, related_name='author')
  guests = models.ManyToManyField(User, through='RSVP')
  category = models.ForeignKey(Category)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
  	return self.title + "(" + str(self.date) + ")"

  class Meta:
  	db_table='event'
  		

class RSVP(models.Model):

	guest = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	date_responded = models.DateTimeField(auto_now_add=True, auto_now=True)
	response = models.CharField(max_length=1, choices=(("A", "Attending"),("N", "Not Attending"), ("M", "May Be Attending")))

	class Meta:
		db_table='rsvp'
		unique_together = (('event','guest'))
