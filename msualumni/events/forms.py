from django import forms
from django.forms import widgets

from events.models import Event

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['title', 'description', 'date', 'time', 'category']
