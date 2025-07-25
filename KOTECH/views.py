from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from Accounts.models import Speaker, Event, ProjectExhibitionRegistration, HackathonRegistration, IdeathonRegistration, MediaRegistration, ReadmissionRegistration
import requests
import re
from django.conf import settings
from django.contrib import messages
from datetime import date, timedelta, datetime

class HackathonRegistrationView(TemplateView):
    template_name = 'hackathon.html'

    def get(self, request):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

    def post(self, request):
        team_lead_name = request.POST.get('team_lead_name')
        other_members = request.POST.get('number_of_members')
        institution = request.POST.get('institution')
        district = request.POST.get('district')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        github_profile = request.POST.get('github_profile')
        linkedin_profile = request.POST.get('linkedin_profile')
        portfolio = request.POST.get('portfolio')
        resume_link = request.POST.get('resume_link')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect('hackathon_registration')

        if not all([team_lead_name, institution, district, email, contact_number, resume_link]):
            messages.error(request, 'All required fields must be filled!')
            return redirect('hackathon_registration')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Invalid email format.')
            return redirect('hackathon_registration')

        if not re.match(r"^\d{10,15}$", contact_number):
            messages.error(request, 'Contact number must be 10 to 15 digits.')
            return redirect('hackathon_registration')

        if not resume_link.startswith(('http://', 'https://')):
            messages.error(request, 'Resume link must be a valid URL.')
            return redirect('hackathon_registration')

        if len(team_lead_name) > 100:
            messages.error(request, 'Team lead name too long.')
            return redirect('hackathon_registration')

        if institution and len(institution) > 150:
            messages.error(request, 'Institution name too long.')
            return redirect('hackathon_registration')

        HackathonRegistration.objects.create(
            team_lead_name=team_lead_name,
            number_of_members=other_members,
            institution=institution,
            district=district,
            email=email,
            contact_number=contact_number,
            github_profile=github_profile,
            linkedin_profile=linkedin_profile,
            portfolio=portfolio,
            resume_link=resume_link,
        )

        return redirect('registration_success')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['speakers'] = Speaker.objects.all()
        context['events'] = Event.objects.filter(pin=True)
        base_date = date(2025, 7, 25)

        day1 = base_date
        day2 = base_date + timedelta(days=1)
        day3 = base_date + timedelta(days=2)

        context['day1_events'] = Event.objects.filter(date=day1).order_by('start_time')
        context['day2_events'] = Event.objects.filter(date=day2).order_by('start_time')
        context['day3_events'] = Event.objects.filter(date=day3).order_by('start_time')
        context['day1_events_pin'] = Event.objects.filter(date=day1, pin=True).order_by('start_time')
        context['day2_events_pin'] = Event.objects.filter(date=day2, pin=True).order_by('start_time')
        context['day3_events_pin'] = Event.objects.filter(date=day3, pin=True).order_by('start_time')

        return context


class LiveView(TemplateView):
    template_name = 'live.html'

    def get_context_data(self, **kwargs):
        context = super(LiveView, self).get_context_data(**kwargs)
        
        # Get current date and time
        now = datetime.now()
        
        # Define the event date range for KOTECH (July 25-27, 2025)
        event_start_date = date(2025, 7, 25)
        event_end_date = date(2025, 7, 27)
        
        # Get all events within the KOTECH event period
        all_events = Event.objects.filter(
            date__gte=event_start_date,
            date__lte=event_end_date
        ).order_by('date', 'start_time')
        
        live_events = []
        upcoming_events = []
        ended_events = []
        
        for event in all_events:
            # Create start and end datetime objects for the event
            event_start_datetime = datetime.combine(event.date, event.start_time)
            
            # Handle end_date logic: if end_date is different from start date, use it
            # Otherwise, assume the event ends on the same day
            if event.end_date and event.end_date != event.date:
                event_end_datetime = datetime.combine(event.end_date, event.end_time)
            else:
                event_end_datetime = datetime.combine(event.date, event.end_time)
            
            # Check if event is currently running
            if event_start_datetime <= now <= event_end_datetime:
                # Event is currently running
                live_events.append(event)
            elif event_start_datetime > now:
                # Event is upcoming
                upcoming_events.append(event)
            else:
                # Event has ended
                ended_events.append(event)
        
        # Sort events by start time for better organization
        live_events.sort(key=lambda x: (x.date, x.start_time))
        upcoming_events.sort(key=lambda x: (x.date, x.start_time))
        ended_events.sort(key=lambda x: (x.date, x.start_time), reverse=True)  # Recent first
        
        context['live_events'] = live_events[:2]  # Limit to 2 live events for hero
        context['all_live_events'] = live_events  # All live events for other sections if needed
        context['upcoming_events'] = upcoming_events[:12]  # Show more upcoming events for 3-day event
        context['ended_events'] = ended_events[:12]  # Show more ended events for 3-day event
        context['hero_upcoming_event'] = upcoming_events[0] if upcoming_events else None  # First upcoming event for hero
        
        # Add additional context for debugging/display
        context['current_datetime'] = now
        context['event_dates'] = {
            'start': event_start_date,
            'end': event_end_date
        }
        
        return context


class MediaRegisterView(TemplateView):
    template_name = 'media_register.html'

    def post(self,request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contact_number')
        Institution = request.POST.get('institution')
        area = request.POST.get('area')
        portfolio = request.POST.get('portfolio')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect('media')
        
        if not all([name, Institution, email, contact_no]):
            messages.error(request, 'All required fields must be filled!')
            return redirect('media')
        
        MediaRegistration.objects.create(
            name = name,
            institution = Institution,
            contact_no = contact_no,
            email = email,
            intrested_area = area,
            portfolio = portfolio,
        )
        return redirect('registration_success')
    def get(self, request):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})


class ReadmissionView(TemplateView):
    template_name = 'readmission.html'

    def post(self,request):
        name = request.POST.get('name')
        age = request.POST.get('age')
        contact_no = request.POST.get('contact_no')
        department = request.POST.get('department')
        muncipality = request.POST.get('muncipality')
        vard = request.POST.get('vard')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect('readmisson')
        
        if not all([name,age, department, muncipality,vard, contact_no]):
            messages.error(request, 'All required fields must be filled!')
            return redirect('readmission')
        
        ReadmissionRegistration.objects.create(
            name = name,
            department = department,
            muncipality = muncipality,
            vard = vard,
            age = age,
            contact_no = contact_no,
        )
        return redirect('registration_success')
    def get(self, request):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
       

class IdeathonRegistrationView(TemplateView):
    template_name = 'ideathon.html'

    def post(self, request):
        team_lead_name = request.POST.get('team_lead_name')
        team_name = request.POST.get('team_name')
        institution = request.POST.get('institution')
        no_of_members = request.POST.get('no_of_members')
        email = request.POST.get('email')
        phone = request.POST.get('contact_number')
        recaptcha_response = request.POST.get('g-recaptcha-response')


        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect('Ideathon')

        if not all([team_lead_name, team_name, institution, no_of_members, email, phone]):
            messages.error(request, 'All required fields must be filled!')
            return redirect('Ideathon')

        try:
            no_of_members = int(no_of_members)
        except ValueError:
            messages.error(request, 'Number of members must be a number!')
            return redirect('register')

        if no_of_members > 4:
            messages.error(request, 'Number of members cannot be more than 4!')
            return redirect('Ideathon')



        IdeathonRegistration.objects.create(
            team_lead_name=team_lead_name,
            team_name=team_name,
            institution=institution,
            number_of_members=no_of_members,
            email=email,
            contact_number=phone,
        )
        return redirect('registration_success')

    def get(self, request):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})




class ExpoRegisterView(TemplateView):
    template_name = 'expo_register.html'

    def post(self, request):
        leader_name = request.POST.get('leader_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        team_name = request.POST.get('team_name')
        number_of_members = request.POST.get('number_of_members')
        description = request.POST.get('description')
        abstract_pdf = request.FILES.get('abstract_pdf')
        district = request.POST.get('district')
        university = request.POST.get('university')
        abstract_link = request.POST.get('abstract_link')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result.get('success'):
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
            return redirect('register')

        if not all([leader_name, email, phone, team_name, number_of_members, abstract_pdf]):
            messages.error(request, 'All fields are required!')
            return redirect('register')

        try:
            number_of_members = int(number_of_members)
        except ValueError:
            messages.error(request, 'Number of members must be a number!')
            return redirect('register')

        if number_of_members > 4:
            messages.error(request, 'Number of members cannot be more than 4!')
            return redirect('register')

        if not abstract_pdf.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are allowed for abstract.')
            return redirect('register')

        ProjectExhibitionRegistration.objects.create(
            leader_name=leader_name,
            email=email,
            phone=phone,
            team_name=team_name,
            number_of_members=number_of_members,
            abstract_pdf=abstract_pdf,
            district=district,
            university=university,
            abstract_link=abstract_link,
        )

        return redirect('registration_success')

    def get(self, request):
        return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})

def under_construction(request):
    return render(request, 'under_construction.html')

def registration_success(request):
    return render(request, 'success.html')

def Register(request):
    return render(request, 'expo_register.html')
