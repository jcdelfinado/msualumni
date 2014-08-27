from django.shortcuts import render, RequestContext
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from urllib import unquote
import sys
import datetime
from models import Event, Category, RSVP

class AddEvent(CreateView):
	model = Event

class EventsByCategory(ListView):
	allow_empty = True
	def get(self, request, *args, **kwargs):
		category = kwargs.get('category')
		cat_name = unquote(category)
		self.category = Category.objects.get(name=cat_name)
		self.queryset = Event.objects.filter(
			is_approved=True,
			date__gte=datetime.date.today(),
			category_id__name__iexact = category
		).order_by("date")

		return super(EventsByCategory, self).get(request, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(EventsByCategory, self).get_context_data(**kwargs)
		print self.category
		context['category'] = self.category
		context['categories'] = Category.objects.only('name').all()
		context['today'] = datetime.date.today()
		return context

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