from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from events.msuadmin.views import (EventsIndex, EventDetails, 
						 UpcomingEvents, EventsByCategory, 
						 reserve, AddEvent,
						 EditEvent)

urlpatterns = patterns('',
    url(r'^$', EventsIndex.as_view()),
    url(r'^details/(?P<pk>\d+)/$', EventDetails.as_view(), name="admin_event_details" ),
    url(r'^category/(?P<category>\S+)/$', EventsByCategory.as_view(), name="admin_event_category" ),
    url(r'^upcoming/$', UpcomingEvents.as_view(), name="admin_upcoming_events"),
    url(r'^edit/(?P<id>\d+)/$', EditEvent.as_view(), name="admin_edit_event"),
    url(r'^rsvp$', reserve),
    url(r'^add$', AddEvent.as_view(), name="add_event")
)
