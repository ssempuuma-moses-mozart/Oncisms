from django.shortcuts import render, redirect
from ministry.models import *
from .models import *
from .forms import *
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from django.db import IntegrityError
from django.db.models import Sum, Count

def home(request):
	schools = School.objects.all().order_by('name')
	context = {
	'title': 'Home',
	'schools':schools,
	}
	return render(request, 'public/home.html', context)

def schools(request, pk):
	schtype = Schtype.objects.get(pk=pk)
	school_list = School.objects.filter(schtype=pk).order_by('name')
	paginator = Paginator(school_list, 1000)
	page = request.GET.get('page')
	schools = paginator.get_page(page)
	context = {
	'title': 'Schools', 
	'schools': schools,
	'schtype':schtype,

	}
	return render(request, 'public/schools.html', context)

def school_levels(request, pk):
	schtype = Level.objects.get(pk=pk)
	school_list = School.objects.filter(level=pk).order_by('name')
	paginator = Paginator(school_list, 1000)
	page = request.GET.get('page')
	schools = paginator.get_page(page)
	context = {
	'title': 'Schools', 
	'schools': schools, 
	'schtype':schtype,

	}
	return render(request, 'public/schools.html', context)

def school(request, pk):
	school = School.objects.get(pk=pk)
	teachers = Teacher.objects.filter(school=school).order_by('-id')
	context = {
	'title': 'Schools', 
	'school': school,
	'teachers': teachers,

	}
	return render(request, 'public/school.html', context)

def teachers(request):
	teacher_list = District.objects.annotate(total_teachers = Count('district')).order_by('-total_teachers')
	paginator = Paginator(teacher_list, 1000)
	page = request.GET.get('page')
	teachers = paginator.get_page(page)
	context = {'title': 'Teachers', 'teachers': teachers}
	return render(request, 'public/teachers.html', context)

def deos(request):
	deo_list = Deo.objects.all().order_by('name')
	paginator = Paginator(deo_list, 1000)
	page = request.GET.get('page')
	deos = paginator.get_page(page)
	return render(request, 'public/DEOs.html', {'title': 'DEOs','deos': deos})

def service_providers(request, pk):
	service = Service.objects.get(pk=pk)
	provider_list = ServiceProvider.objects.filter(service=pk, status=2).order_by('name')
	paginator = Paginator(provider_list, 1000)
	page = request.GET.get('page')
	service_providers = paginator.get_page(page)
	context = {
	'title': 'Service Providers', 
	'service_providers': service_providers, 
	'service':service,

	}
	return render(request, 'public/service_providers.html', context)

def apply(request):
	if request.method == 'POST':
		apply_form = ApplyCreateForm(request.POST, request.FILES,)
		if apply_form.is_valid():
			try:
				apply_form.save()
				messages.success(request, f'Thank you! You have applied to be added as a service provider.')
				return HttpResponseRedirect(reverse('apply'))
			except Exception:
				messages.warning(request, f'Error! Your application did not complete!')		
	else:
		apply_form = ApplyCreateForm()

	context = {
	'title': 'Service Providers',
	'apply_form': apply_form,
	}

	return render(request, 'public/apply_form.html', context)

def covid19(request):
	classes = Classe.objects.annotate(uploads=Count('lockdownpackage')).order_by('id')
	return render(request, 'public/covid19.html', {'title': 'COVID-19','classes': classes})

def covid19_downloads(request, pk):
	the_class = Classe.objects.get(pk=pk)
	uploads = LockdownPackage.objects.filter(home_class=the_class).order_by('-id')
	classes = Classe.objects.annotate(uploads=Count('lockdownpackage')).exclude(pk=pk).order_by('id')
	context = {
	'title': 'COVID-19',
	'classes': classes,
	'the_class': the_class,
	'uploads': uploads, 
	}
	return render(request, 'public/covid19_downloads.html', context)


def results(request):
	return render(request, 'public/results.html', {'title': 'UNEB Results'})

def marketing(request):
	return render(request, 'public/marketing.html', {'title': 'Marketing'})

def communication(request):
	return render(request, 'public/communication.html', {'title': 'Communication'})

def resources(request):
	return render(request, 'public/resources.html', {'title': 'Resources'})

def settings(request):
	return render(request, 'public/settings.html', {'title': 'Settings'})

class SliderTemplate(TemplateView):
	template_name = 'public/slider.html'

class SliderMainTemplate(TemplateView):
	template_name = 'public/slider_main.html'
