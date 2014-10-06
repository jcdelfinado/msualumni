from django.shortcuts import render, RequestContext
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse
from forms import EventForm
from urllib import unquote
import sys
import datetime
from models import Event, Category, RSVP

class AddEvent(CreateView):
	model = Event
	form_class = EventForm
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(AddEvent, self).form_valid(form)

	def get_success_url(self):
		success_url = "/events/details/"+str(self.object.id)
		if self.request.user.is_staff:
			success_url = "/admin"+success_url
		return success_url

class EditEvent(UpdateView):
	form_class = EventForm

	def get(self, request, **kwargs):
		self.object = Event.objects.get(id=self.kwargs['id'])
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(object=self.object, form=form)
		return self.render_to_response(context)

	def get_object(self, queryset=None):
	    obj = Event.objects.get(id=self.kwargs['id'])
	    return obj

	def get_success_url(self, **kwargs):
		from django.core.urlresolvers import resolve
		current_url = resolve(self.request.path_info).url_name
		base_url = '/events/details/'
		if current_url == 'admin-edit-event':
			base_url = '/admin' + base_url
		print base_url
		return base_url + str(self.object.id)

class EventsByCategory(ListView):
	allow_empty = True
	def get(self, request, *args, **kwargs):
		category = kwargs.get('category')
		cat_name = unquote(category)
		self.category = Category.objects.get(name=cat_name)
		self.queryset = Event.objects.filter(
			is_approved=True,
			date__gte=datetime.date.today(),
			category_id = self.category.id
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
		print RSVP.objects.only('guest_id').filter(event_id = self.object.id).values()
		context['attending'] = RSVP.objects.only('guest_id').filter(event_id=self.object.id, guest_id=self.request.user.id).exists()
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
			return HttpResponse('You have successfully reserved for this event')
	except:
		print sys.exc_info()[0], sys.exc_info()[1]
		return HttpResponse('There was an error processing your request')