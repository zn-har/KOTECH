from django.http import HttpRequest
from django.shortcuts import render , redirect
from django.views.generic import TemplateView
from Accounts.models import Speaker, Event, EventRegistration


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['speakers'] = Speaker.objects.all()
        context['events'] = Event.objects.all()
        return context


def register_expo(request):
    if request.method == 'POST':
        name = request.POST.get('leader_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        team_name = request.POST.get('team_name')
        number_of_members = request.POST.get('number_of_members')
        description = request.POST.get('description')
        abstract_pdf = request.FILES.get('abstract_pdf')

        # --- Basic validations ---
        if not all([name, email, phone, team_name, number_of_members, description, abstract_pdf]):
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
            name=name,
            email=email,
            phone=phone,
            team_name=team_name,
            number_of_members=number_of_members,
            description=description,
            abstract_pdf=abstract_pdf
        )

        return redirect('registration_success')

    return render(request, 'expo_register.html')


def registration_success(request):
    return render(request, 'registration_success.html')


def Register(request):
    return render(request, 'expo_register.html')
