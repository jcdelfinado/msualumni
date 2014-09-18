from django.contrib import admin as dj_admin
from models import Alum, Program, College, Campus, Graduation, ProfileApplication

dj_admin.site.register(Alum)

dj_admin.site.register(Campus)
dj_admin.site.register(College)
dj_admin.site.register(Program)
dj_admin.site.register(Graduation)
dj_admin.site.register(ProfileApplication)
