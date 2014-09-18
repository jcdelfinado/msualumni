from django import forms
from django.forms import widgets

from events.models import Event

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['title', 'venue', 'description', 'date', 'time', 'category']
		widgets = {
			'date' : forms.TextInput(attrs={'type':'date'}),
			'description' : forms.Textarea(attrs={'rows':8})
		}
