from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from Accounts.models import Speaker, Event


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['speakers'] = Speaker.objects.all()
        context['events'] = Event.objects.all()
        return  context