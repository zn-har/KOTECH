from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView , View
from Accounts.models import Speaker, Event, EventRegistration, HackathonRegistration
import requests
import re
from django.conf import settings
from django.contrib import messages


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
            return render(request, self.template_name, {'error': 'All required fields must be filled!'})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render(request, self.template_name, {'error': 'Invalid email format.'})

        if not re.match(r"^\d{10,15}$", contact_number):
            return render(request, self.template_name, {'error': 'Contact number must be 10 to 15 digits.'})

        if not resume_link.startswith(('http://', 'https://')):
            return render(request, self.template_name, {'error': 'Resume link must be a valid URL.'})

        if len(team_lead_name) > 100:
            return render(request, self.template_name, {'error': 'Team lead name too long.'})

        if institution and len(institution) > 150:
            return render(request, self.template_name, {'error': 'Institution name too long.'})

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
		context['events'] = Event.objects.all()
		return context


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


		# Verify reCAPTCHA
		data = {
			'secret': settings.RECAPTCHA_PRIVATE_KEY,
			'response': recaptcha_response
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result = r.json()

		if not result.get('success'):
			messages.error(request, "Invalid reCAPTCHA. Please try again.")
			return redirect('register')

		# --- Basic validations ---
		if not all([leader_name, email, phone, team_name, number_of_members, description, abstract_pdf]):
			return render(request, 'expo_register.html', {'error': 'All fields are required!'})

		if int(number_of_members) > 4:
			return redirect("register")

		if len(description) > 300:
			return render(request, 'expo_register.html', {'error': 'Description must be 300 characters or less.'})

		try:
			number_of_members = int(number_of_members)
		except ValueError:
			return render(request, 'expo_register.html', {'error': 'Number of members must be a number!'})

		if not abstract_pdf.name.endswith('.pdf'):
			return render(request, 'expo_register.html', {'error': 'Only PDF files are allowed for abstract.'})

		# --- Save the object ---
		registration = EventRegistration.objects.create(
			leader_name=leader_name,
			email=email,
			phone=phone,
			team_name=team_name,
			number_of_members=number_of_members,
			description=description,
			abstract_pdf=abstract_pdf,
			district=district,
			university=university,
			abstract_link=abstract_link,


		)

		return redirect('registration_success')

	def get(self, request):
		return render(request, self.template_name, {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})


def registration_success(request):
	return render(request, 'success.html')


def Register(request):
	return render(request, 'expo_register.html')
