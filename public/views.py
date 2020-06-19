from django.shortcuts import render
from ministry.models import *
from django.core.paginator import Paginator
def home(request):
	schools = School.objects.all().order_by('name')
	context = {
	'title': 'Home',
	'schools':schools,
	}
	return render(request, 'public/home.html', context)

def schools(request):
	school_list = School.objects.all().order_by('name')
	total_schools = School.objects.count()
	paginator = Paginator(school_list, 1000)
	page = request.GET.get('page')
	schools = paginator.get_page(page)
	return render(request, 'public/schools.html', {'title': 'Schools', 'schools': schools, 'total_schools': total_schools})

def teachers(request):
	teacher_list = Teacher.objects.all().order_by('name')
	total_teachers = Teacher.objects.count()
	paginator = Paginator(teacher_list, 1000)
	page = request.GET.get('page')
	teachers = paginator.get_page(page)
	return render(request, 'public/teachers.html', {'title': 'Teachers', 'teachers': teachers})

def deos(request):
	deo_list = Deo.objects.all().order_by('name')
	total_deos = Deo.objects.count()
	paginator = Paginator(deo_list, 1000)
	page = request.GET.get('page')
	deos = paginator.get_page(page)
	return render(request, 'public/DEOs.html', {'title': 'DEOs','deos': deos})

def results(request):
	return render(request, 'public/results.html', {'title': 'UNEB Results'})

def marketing(request):
	return render(request, 'public/marketing.html', {'title': 'Marketing'})

def communication(request):
	return render(request, 'public/communication.html', {'title': 'Communication'})

def settings(request):
	return render(request, 'public/settings.html', {'title': 'Settings'})
