from django.shortcuts import render, RequestContext
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
import sys
import datetime
from models import Event, Category, RSVP

class EventsIndex(ListView):
	queryset = Event.objects.filter(
			is_approved=True,
			date__gte=datetime.date.today()
		).order_by("date")
	allow_empty = True
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(EventsIndex, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['today'] = datetime.date.today()
		print context
		return context

class UpcomingEvents(ListView):
	queryset = Event.objects.filter(
			is_approved=True,
			date__gte=datetime.date.today()
		).order_by("date")
	allow_empty = True

	def get_context_data(self, **kwargs):
		context = super(UpcomingEvents, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['today'] = datetime.date.today()
		print context
		return context

class EventDetails(DetailView):
	model = Event

	def get_context_data(self, **kwargs):
		context = super(EventDetails, self).get_context_data(**kwargs)
		context['attendance'] = RSVP.objects.filter(event_id = self.object.id).count()
		return context

def reserve(request):
	context = RequestContext(request)
	try:
		if request.method == 'POST':
			guest_id = request.POST['id']
			event_id = request.POST['event']
			reservation = RSVP(
				event_id = event_id,
				guest_id = guest_id,
				response = 'A'
				)
			reservation.save()
			return HttpResponse('Success',context, status=200)
	except:
		print sys.exc_info()[0], sys.exc_info()[1]