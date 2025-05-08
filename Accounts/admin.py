from django.contrib import admin

from Accounts.models import Speaker, Event, Venue, User, ProjectExhibitionRegistration, HackathonRegistration, IdeathonRegistration

admin.site.site_header = "KOTECH Administration"
admin.site.site_title = "KOTECH Administration"
admin.site.index_title = "Welcome to KOTECH Administration"

admin.site.register(Speaker)
admin.site.register(ProjectExhibitionRegistration)
admin.site.register(IdeathonRegistration)
admin.site.register(HackathonRegistration)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(User)


