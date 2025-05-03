from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from Accounts.models import Speaker, Event, EventRegistration
import requests
from django.conf import settings
from django.contrib import messages


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
