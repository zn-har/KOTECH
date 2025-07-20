from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from Accounts.models import Speaker, Event, ProjectExhibitionRegistration, HackathonRegistration, IdeathonRegistration, MediaRegistration, ReadmissionRegistration
import requests
import re
from django.conf import settings
from django.contrib import messages
from datetime import date, timedelta

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

        context['day1_events'] = Event.objects.filter(date=day1).order_by('time')
        context['day2_events'] = Event.objects.filter(date=day2).order_by('time')
        context['day3_events'] = Event.objects.filter(date=day3).order_by('time')
        context['day1_events_pin'] = Event.objects.filter(date=day1, pin=True).order_by('time')
        context['day2_events_pin'] = Event.objects.filter(date=day2, pin=True).order_by('time')
        context['day3_events_pin'] = Event.objects.filter(date=day3, pin=True).order_by('time')

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
