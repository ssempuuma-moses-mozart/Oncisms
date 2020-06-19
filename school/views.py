from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)

from ministry.models import *
from users.models import *
from .models import *

class SchoolCreateView(LoginRequiredMixin, CreateView):
	model = School
	template_name = "school/add_profile.html"
	fields = ['name','motto','email','yr_est','regstatus','reg_no','yr_reg','cen_no',
	'cennostatus','yr_cnr','schtype','level','access','category','section',
	'ownership','district','logo']

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('set-school-profile')

class SchoolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = School
	template_name = "school/add_profile.html"
	fields = ['name','motto','email','yr_est','regstatus','reg_no','yr_reg','cen_no',
	'cennostatus','yr_cnr','schtype','level','access','category','section',
	'ownership','district','region','logo'] 

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('set-school-profile')

	def test_func(self):
		school = SchoolProfile.objects.filter(user=self.request.user).first()
		if self.request.user == school.user:
			return True
		return False

class SetProfileCreateView(LoginRequiredMixin, CreateView):
	model = SchoolProfile
	template_name = "school/set_profile.html"
	fields =['school']

	def get_context_data(self, **kwargs):
		context = super(SetProfileCreateView, self).get_context_data(**kwargs)
		context["title"] = "Settings"
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('school-profile')

class SchoolTeacherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = SchoolTeacher
	template_name = "school/add_teacher.html"
	fields = ['teacher','on_payroll','status','year_since']

	def get_context_data(self, **kwargs):
		context = super(SchoolTeacherCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-teacher')

	def test_func(self):
		school = SchoolProfile.objects.filter(user=self.request.user).first()
		if school:
			if self.request.user.groups.values_list('id', flat=True).last() == settings.SCHOOL_GROUP_ID:
				return True
			return False
		return False

class TeacherCreateView(LoginRequiredMixin, CreateView):
	model = Teacher
	template_name = "school/register_teacher.html"
	fields =['name','reg_no','email','status','gender','date_registered','district','region','photo']

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-teacher')

class SchoolTeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = SchoolTeacher
	template_name = "school/add_teacher.html"
	fields = ['teacher','on_payroll','status','year_since']
	def get_context_data(self, **kwargs):
		context = super(SchoolTeacherUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-teacher')

	def test_func(self):
		teacher = self.get_object()
		if self.request.user == teacher.user:
			return True
		return False

class SchoolTeacherListView(ListView):
	model = SchoolTeacher
	template_name = "school/view_teachers.html"
	def get_context_data(self, **kwargs):
		context = super(SchoolTeacherListView, self).get_context_data(**kwargs)
		context["teachers"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

class SchoolTeacherDetailView(DetailView):
	model = SchoolTeacher
	template_name = "school/teacher_detail.html"

class SchoolResourceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = SchoolResource
	template_name = "school/add_resource.html"
	fields =['resource','quantity','amount','year']

	def get_context_data(self, **kwargs):
		context = super(SchoolResourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-resource')

	def test_func(self):
		school = SchoolProfile.objects.filter(user=self.request.user).first()
		if school:
			if self.request.user.groups.values_list('id', flat=True).last() == settings.SCHOOL_GROUP_ID:
				return True
			return False
		return False

class SchoolResourceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = SchoolResource
	template_name = "school/add_resource.html"
	fields =['resource','quantity','amount','year']

	def get_context_data(self, **kwargs):
		context = super(SchoolResourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		school_resources = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["school_resources"] = school_resources.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-resource')

	def test_func(self):
		resource = self.get_object()
		if self.request.user == resource.user:
			return True
		return False

class SchoolResourceListView(ListView):
	model = SchoolResource
	template_name = "school/view_resources.html"
	def get_context_data(self, **kwargs):
		context = super(SchoolResourceListView, self).get_context_data(**kwargs)
		context["resources"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

class SchoolResourceDetailView(DetailView):
	model = SchoolResource
	template_name = "school/resource_details.html"

class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Student
	template_name = "school/add_students.html"
	fields =['class_name','no_of_students','year']

	def get_context_data(self, **kwargs):
		context = super(StudentCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		students = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["students"] = students.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-students')

	def test_func(self):
		school = SchoolProfile.objects.filter(user=self.request.user).first()
		if school:
			if self.request.user.groups.values_list('id', flat=True).last() == settings.SCHOOL_GROUP_ID:
				return True
			return False
		return False

class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Student
	template_name = "school/add_students.html"
	fields =['class_name','no_of_students','year']

	def get_context_data(self, **kwargs):
		context = super(StudentUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		students = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["students"] = students.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-students')

	def test_func(self):
		student = self.get_object()
		if self.request.user == student.user:
			return True
		return False

class StudentListView(ListView):
	model = Student
	template_name = "school/view_students.html"
	def get_context_data(self, **kwargs):
		context = super(StudentListView, self).get_context_data(**kwargs)
		context["students"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

class RequestTeacherCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = RequestTeacher
	template_name = "school/requestteacher_form.html"
	fields =['subject','level','comment']

	def get_context_data(self, **kwargs):
		context = super(RequestTeacherCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teacher_requests = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["teacher_requests"] = teacher_requests.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('request-teacher')

	def test_func(self):
		school = SchoolProfile.objects.filter(user=self.request.user).first()
		if school:
			if self.request.user.groups.values_list('id', flat=True).last() == settings.SCHOOL_GROUP_ID:
				return True
			return False
		return False

class RequestTeacherUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = RequestTeacher
	template_name = "school/requestteacher_form.html"
	fields =['subject','level','comment']

	def get_context_data(self, **kwargs):
		context = super(RequestTeacherUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teacher_requests = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["teacher_requests"] = teacher_requests.get_page(page)
		return context

	def form_valid(self, form):
		form.save()
		return redirect('request-teacher')

	def test_func(self):
		req = self.get_object()
		if self.request.user == req.user:
			return True
		return False

class RequestTeacherListView(ListView):
	model = RequestTeacher
	def get_context_data(self, **kwargs):
		context = super(RequestTeacherListView, self).get_context_data(**kwargs)
		context["teacher_requests"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

class RequestResourceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = RequestResource
	template_name = "school/requestresource_form.html"
	fields =['resource','reason','comment']

	def get_context_data(self, **kwargs):
		context = super(RequestResourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resource_requests = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["resource_requests"] = resource_requests.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('request-resource')

	def test_func(self):
		school = SchoolProfile.objects.filter(user=self.request.user).first()
		if school:
			if self.request.user.groups.values_list('id', flat=True).last() == settings.SCHOOL_GROUP_ID:
				return True
			return False
		return False

class RequestResourceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = RequestTeacher
	template_name = "school/requestresource_form.html"
	fields =['resource','reason','comment']

	def get_context_data(self, **kwargs):
		context = super(RequestResourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resource_requests = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["resource_requests"] = resource_requests.get_page(page)
		return context

	def form_valid(self, form):
		form.save()
		return redirect('request-resource')

	def test_func(self):
		req = self.get_object()
		if self.request.user == req.user:
			return True
		return False

class RequestResourceListView(ListView):
	model = RequestResource
	def get_context_data(self, **kwargs):
		context = super(RequestResourceListView, self).get_context_data(**kwargs)
		context["resource_requests"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

def home(request):
	school_profile = SchoolProfile.objects.filter(user=request.user).first()
	return render(request, 'school/home.html', {'title': 'Home', 
		'schools':school_profile,  })

def teachers(request):
	school_teachers = SchoolTeacher.objects.filter(user=request.user)
	return render(request, 'school/teachers.html', {'title': 'Teachers', 
		'school_teachers':school_teachers,  })

def profile(request):
	profiles = SchoolProfile.objects.filter(user=request.user)
	return render(request, 'school/profile.html', {'title': 'Profile', 
		'profiles':profiles, })

def resources(request):
	school_resources = SchoolResource.objects.filter(user=request.user)
	return render(request, 'school/resources.html', {'title': 'Resources', 
		'school_resources':school_resources,  })

def students(request):
	students = Student.objects.filter(user=request.user)
	return render(request, 'school/students.html', {'title': 'Students', 
		'students':students,  })