from django.contrib import admin

from Accounts.models import Speaker, Event, Venue, User, ProjectExhibitionRegistration, HackathonRegistration

admin.site.register(Speaker)
admin.site.register(ProjectExhibitionRegistration)
admin.site.register(HackathonRegistration)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(User)


