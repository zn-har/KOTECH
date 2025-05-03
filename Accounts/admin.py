from django.contrib import admin

from Accounts.models import Speaker, Event, Venue, User, EventRegistration 

admin.site.register(Speaker)
admin.site.register(EventRegistration)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(User)


