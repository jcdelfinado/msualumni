from django.conf.urls import patterns, include, url

from events.views import (EventsIndex, EventDetails, 
						 UpcomingEvents, EventsByCategory, 
						 reserve, AddEvent,
						 EditEvent)

urlpatterns = patterns('',
    url(r'^$', EventsIndex.as_view(template_name="events/msuadmin/index.html")),
    url(r'^details/(?P<pk>\d+)/$', EventDetails.as_view(template_name = "events/msuadmin/event_detail.html"), name="event-details" ),
    url(r'^category/(?P<category>\S+)/$', EventsByCategory.as_view(template_name = "events/msuadmin/event_by_category.html"), name="event_category" ),
    url(r'^upcoming/$', UpcomingEvents.as_view(template_name="events/msuadmin/upcoming.html"), name="upcoming-events"),
    url(r'^edit/(?P<id>\d+)/$', EditEvent.as_view(template_name="events/msuadmin/edit_event.html"), name="admin-edit-event"),
    url(r'^rsvp$', reserve),
    url(r'^add$', AddEvent.as_view(template_name="events/msuadmin/add_event.html"), name="add_event")
)
