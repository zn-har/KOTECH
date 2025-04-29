from django.contrib import admin

from Accounts.models import Speaker, Event, Venue, User

admin.site.register(Speaker)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(User)


