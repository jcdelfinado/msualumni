from events.views import *
from portal.access import MSUAdminMixin

class AddEvent(MSUAdminMixin, AddEvent):
	template_name="events/msuadmin/add_event.html"

class EditEvent(MSUAdminMixin, EditEvent):
	template_name="events/msuadmin/edit_event.html"

class EventsByCategory(MSUAdminMixin, EventsByCategory):
	template_name = "events/msuadmin/event_by_category.html"

class EventsIndex(MSUAdminMixin, EventsIndex):
	template_name="events/msuadmin/index.html"

class UpcomingEvents(MSUAdminMixin, UpcomingEvents):
	template_name="events/msuadmin/upcoming.html"

class EventDetails(MSUAdminMixin, EventDetails):
	template_name = "events/msuadmin/event_detail.html"

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