from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
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
from .forms import *
import datetime
from django.db.models import Sum
from django.db.models import  Q, Count

class SchoolCreateView(LoginRequiredMixin, CreateView):
	model = School
	template_name = "ministry/school_form.html"
	fields = ['name','motto','phone','website','email','box_no','parish','address','fax','service_code','yr_est',
			'regstatus','reg_no','cen_no','level','highest_class','access','category','section','founder',
			'funder','operation_status','distance_to_nearest_school','distance_to_deo_office','logo']
	def get_context_data(self, **kwargs):
		context = super(SchoolCreateView, self).get_context_data(**kwargs)
		context["title"] = "Settings"
		context["parishes"] = Parish.objects.all()
		context["regstatuses"] = Regstatus.objects.all()
		context["schtypes"] = Schtype.objects.all()
		context["founders"] = Ownership.objects.all()
		context["funders"] = Funder.objects.all()
		context["accesses"] = Access.objects.all()
		context["rural_urban"] = RuralUrban.objects.all()
		context["categories"] = Category.objects.all()
		context["sections"] = Section.objects.all()
		context["levels"] = Level.objects.all()
		context["classes"] = Class.objects.all()
		context["dns"] = DistanceToNearestSchool.objects.all()
		context["ddo"] = DistanceToDeoOffice.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		school = form.save()
		school_profile = SchoolProfile.objects.create(user=self.request.user, school=school, group=4)
		return redirect('school-home')

class SchoolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = School
	template_name = "ministry/school_form.html"
	fields = ['name','motto','phone','website','email','box_no','parish','address','fax','service_code','yr_est',
			'regstatus','reg_no','cen_no','level','highest_class','access','category','section','founder',
			'funder','operation_status','distance_to_nearest_school','distance_to_deo_office','logo'] 
	def get_context_data(self, **kwargs):
		context = super(SchoolUpdateView, self).get_context_data(**kwargs)
		context["title"] = "Settings"
		context["parishes"] = Parish.objects.all()
		context["regstatuses"] = Regstatus.objects.all()
		context["schtypes"] = Schtype.objects.all()
		context["founders"] = Ownership.objects.all()
		context["funders"] = Funder.objects.all()
		context["accesses"] = Access.objects.all()
		context["rural_urban"] = RuralUrban.objects.all()
		context["categories"] = Category.objects.all()
		context["sections"] = Section.objects.all()
		context["levels"] = Level.objects.all()
		context["classes"] = Class.objects.all()
		context["dns"] = DistanceToNearestSchool.objects.all()
		context["ddo"] = DistanceToDeoOffice.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('school-home')

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

class SchoolTeacherListView(LoginRequiredMixin, ListView):
	model = SchoolTeacher
	template_name = "school/view_teachers.html"
	def get_context_data(self, **kwargs):
		context = super(SchoolTeacherListView, self).get_context_data(**kwargs)
		context["teachers"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

class SchoolTeacherDetailView(LoginRequiredMixin, DetailView):
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

class SchoolResourceListView(LoginRequiredMixin, ListView):
	model = SchoolResource
	template_name = "school/view_resources.html"
	def get_context_data(self, **kwargs):
		context = super(SchoolResourceListView, self).get_context_data(**kwargs)
		context["resources"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

class SchoolResourceDetailView(LoginRequiredMixin, DetailView):
	model = SchoolResource
	template_name = "school/resource_details.html"

@login_required
def add_students(request):
	students = Student.objects.filter(user=request.user,).order_by('-id',)[:10]
	classes = None
	ages = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	if(request.user.schoolprofile.school.level_id==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(request.user.schoolprofile.school.level_id==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=12,)
	elif(request.user.schoolprofile.school.level_id==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=22,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)

	# if request.method == 'POST':
	# 	student_form = StudentCreateForm(request.POST, request.FILES)
	# 	if student_form.is_valid():
	# 		student_form.instance.user = request.user
	# 		student_form.save(commit=False)
	# 		if 'save_enrolment' in request.POST:
	# 			try:
	# 				student_form.save()
	# 				messages.success(request, f'You have added new set of enrolment.')
	# 				return HttpResponseRedirect(reverse('add-students'))
	# 			except Exception:
	# 				messages.warning(request, f'Error! May be Contact admin')
	enrolment_list = []
	total_rows = len(classes)*len(ages)
	if request.method == 'POST':
		student_form = StudentCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			age = request.POST.getlist('age')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, age, boys, girls]
			enrolment_list.append(std_records)
			for c, a, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(Student(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'age' : Age.objects.get(pk=a[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			# Student.objects.bulk_create(some_data)
			try:
				Student.objects.bulk_create(some_data)
				messages.success(request, f'Enrolments for {year} have been recorded')
			except Exception:
				messages.warning(request, f'ERROR! May be some enrolments of {year} are already readed. Only Fill the ones that are not yet yet entered.')				
	else:
		student_form = StudentCreateForm()
	context = {
	'title': 'Students',
	'students': students,  
	'student_form': student_form,
	'classes': classes,
	'ages': ages,
	}
	return render(request, 'school/add_students.html', context)

class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Student
	template_name = "school/add_students.html"
	form_class = StudentCreateForm

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

@login_required
def view_students(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Student.objects.filter(user=request.user, year=year).order_by('age_id',)
	students_by_class = Student.objects.values('class_name').filter(user=request.user, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_age = Student.objects.values('age').filter(user=request.user, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Student.objects.filter(user=request.user, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	ages = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	if(request.user.schoolprofile.school.level_id==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(request.user.schoolprofile.school.level_id==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=12,)
	elif(request.user.schoolprofile.school.level_id==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=22,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)

	context = {
	'title': 'Students',
	'students': students,
	'classes': classes,
	'ages': ages,
	'students_by_class': students_by_class,
	'students_by_age': students_by_age,
	'total_students': total_students,
	'year':year
	}
	return render(request, 'school/view_students.html', context)

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

class RequestTeacherListView(LoginRequiredMixin, ListView):
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

class RequestResourceListView(LoginRequiredMixin, ListView):
	model = RequestResource
	def get_context_data(self, **kwargs):
		context = super(RequestResourceListView, self).get_context_data(**kwargs)
		context["resource_requests"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context

@login_required
def home(request):
	school_profile = SchoolProfile.objects.filter(user=request.user).first()
	return render(request, 'school/home.html', {'title': 'Home', 
		'schools':school_profile,  })

@login_required
def teachers(request):
	school_teachers = SchoolTeacher.objects.filter(user=request.user)
	return render(request, 'school/teachers.html', {'title': 'Teachers', 
		'school_teachers':school_teachers,  })

@login_required
def profile(request):
	profiles = SchoolProfile.objects.filter(user=request.user)
	return render(request, 'school/profile.html', {'title': 'Profile', 
		'profiles':profiles, })

@login_required
def resources(request):
	school_resources = SchoolResource.objects.filter(user=request.user)
	return render(request, 'school/resources.html', {'title': 'Resources', 
		'school_resources':school_resources,  })

@login_required
def students(request):
	students = Student.objects.filter(user=request.user)
	return render(request, 'school/students.html', {'title': 'Students', 
		'students':students,  })