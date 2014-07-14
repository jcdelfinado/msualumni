#urls for portal
from django.conf.urls import patterns, include, url
from django.contrib import admin as django_admin
from django.contrib.auth import views as auth_views

from views import register, activate

urlpatterns = patterns('',
  url(r'^register$', register),
  url(r'^activate$', activate),
)