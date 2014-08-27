from django.conf.urls import patterns, include, url

from views import EventsIndex, EventDetails, UpcomingEvents, EventsByCategory, reserve, AddEvent

urlpatterns = patterns('',
    url(r'^$', EventsIndex.as_view(template_name="events/index.html")),
    url(r'^details/(?P<pk>\d+)/$', EventDetails.as_view(template_name = "events/event_detail.html"), name="event-details" ),
    url(r'^category/(?P<category>\S+)/$', EventsByCategory.as_view(template_name = "events/event_by_category.html"), name="event_category" ),
    url(r'^upcoming/$', UpcomingEvents.as_view(template_name="events/upcoming.html"), name="upcoming-events"),
    url(r'^rsvp$', reserve),
    url(r'^add$', AddEvent.as_view(template_name="events/add_event.html"), name="add_event")
)
