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
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

# session_key = '8cae76c505f15432b48c8292a7dd0e54'

# session = Session.objects.get(session_key=session_key)
# uid = session.get_decoded().get('_auth_user_id')
# user = User.objects.get(pk=uid)

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
		teachers = Paginator(self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-teacher')

	def test_func(self):
		school = SchoolProfile.objects.filter(school=self.request.user.schoolprofile.school).first()
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
		teachers = Paginator(self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id'), 10)
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
		context["teachers"] = self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id')
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
		resources = Paginator(self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('add-school-resource')

	def test_func(self):
		school = SchoolProfile.objects.filter(school=self.request.user.schoolprofile.school).first()
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
		school_resources = Paginator(self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id'), 10)
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
		context["resources"] = self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id')
		return context

class SchoolResourceDetailView(LoginRequiredMixin, DetailView):
	model = SchoolResource
	template_name = "school/resource_details.html"

@login_required
def add_students(request):
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
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'age' : AgeGroup.objects.get(pk=a[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			# Student.objects.bulk_create(some_data)
			try:
				Student.objects.bulk_create(some_data)
				messages.success(request, f'Enrolments for {year} have been recorded. Proceed to record Repeaters')
				return redirect('add-repeaters')
			except Exception:
				messages.warning(request, f'ERROR! May be some enrolments of {year} are already recorded. Only Fill the ones that are not yet entered.')				
	else:
		student_form = StudentCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Enrolment',
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
		students = Paginator(self.model.objects.filter(school=self.request.user.schoolprofile.school).order_by('-id'), 10)
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
	students = Student.objects.filter(school=request.user.schoolprofile.school, year=year).order_by('age_id',)
	students_by_class = Student.objects.values('class_name').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_age = Student.objects.values('age').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Student.objects.filter(school=request.user.schoolprofile.school, 
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
	'sub_title': 'Enrolment',
	'students': students,
	'classes': classes,
	'ages': ages,
	'students_by_class': students_by_class,
	'students_by_age': students_by_age,
	'total_students': total_students,
	'year':year
	}
	return render(request, 'school/view_students.html', context)

@login_required
def add_repeaters(request):
	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)
	if request.method == 'POST':
		student_form = RepeaterCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, boys, girls]
			enrolment_list.append(std_records)
			for c, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(Repeater(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				Repeater.objects.bulk_create(some_data)
				messages.success(request, f'Repeaters for {year} have been recorded. Proceed to record enrolments by Nationality.')
				return redirect('add-nationality')
			except Exception:
				messages.warning(request, f'ERROR! May be some Repeaters of {year} are already recorded. Only Fill the ones that are not yet recorded.')				
	else:
		student_form = RepeaterCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Repeaters',
	'student_form': student_form,
	'classes': classes,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_nationality(request):
	classes = None
	countries = Country.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)*len(countries)
	if request.method == 'POST':
		student_form = NationalityCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			country = request.POST.getlist('country')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, country, boys, girls]
			enrolment_list.append(std_records)
			for c, a, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(Nationality(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'country' : Country.objects.get(pk=a[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				Nationality.objects.bulk_create(some_data)
				messages.success(request, f'Enrolments for {year} have been recorded. Proceed to record Proposed Intake')
				return redirect('add-proposed-intake')
			except Exception:
				messages.warning(request, f'ERROR! May be some enrolments of {year} are already recorded. Only Fill the ones that are not yet entered.')				
	else:
		student_form = NationalityCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Nationality',
	'student_form': student_form,
	'classes': classes,
	'countries': countries,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_physical_streams(request):
	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)
	if request.method == 'POST':
		student_form = PhysicalStreamCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			streams = request.POST.getlist('streams')
			std_records = [class_name, streams]
			enrolment_list.append(std_records)
			for c, g in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if int(g[i])>0:
						some_data.append(PhysicalStream(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'streams' : g[i],
	                                        }))
			try:
				PhysicalStream.objects.bulk_create(some_data)
				messages.success(request, f'Physical Streams of classes by {year} have been recorded. Proceed to record Orphans')
				return redirect('add-orphans')
			except Exception:
				messages.warning(request, f'ERROR! May be Streams of classes by {year} are already recorded. Only Fill the ones that are not yet recorded.')				
	else:
		student_form = PhysicalStreamCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Physical Streams',
	'student_form': student_form,
	'classes': classes,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_orphans(request):
	classes = None
	statuses = OrphanStatus.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)*len(statuses)
	if request.method == 'POST':
		student_form = OrphanCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			status = request.POST.getlist('status')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, status, boys, girls]
			enrolment_list.append(std_records)
			for c, a, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(Orphan(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'status' : OrphanStatus.objects.get(pk=a[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				Orphan.objects.bulk_create(some_data)
				messages.success(request, f'Orphans for {year} have been recorded. Proceed to record Pupils with special learning needs.')
				return redirect('add-special-needs')
			except Exception:
				messages.warning(request, f'ERROR! May be some Orphans of {year} are already recorded. Only Fill the ones that are not yet entered.')				
	else:
		student_form = OrphanCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Orphans',
	'student_form': student_form,
	'classes': classes,
	'statuses': statuses,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_special_needs(request):
	classes = None
	statuses = SpecialNeedStatus.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)*len(statuses)
	if request.method == 'POST':
		student_form = SpecialNeedCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			status = request.POST.getlist('status')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, status, boys, girls]
			enrolment_list.append(std_records)
			for c, a, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(SpecialNeed(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'status' : SpecialNeedStatus.objects.get(pk=a[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				SpecialNeed.objects.bulk_create(some_data)
				messages.success(request, f'Pupils with Special Learning Needs for {year} have been recorded. Proceed to record New Entrants.')
				return redirect('add-new-entrants')
			except Exception:
				messages.warning(request, f'ERROR! May be some Pupils with Special Learning Needs for {year} are already recorded. Only Fill the ones that are not yet entered.')				
	else:
		student_form = SpecialNeedCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Special Needs',
	'student_form': student_form,
	'classes': classes,
	'statuses': statuses,
	}
	return render(request, 'school/add_students.html', context)



@login_required
def add_seating_and_writing_space(request):
	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)
	if request.method == 'POST':
		student_form = SeatingAndWritingSpaceCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			pupils = request.POST.getlist('pupils')
			std_records = [class_name, pupils]
			enrolment_list.append(std_records)
			for c, g in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if int(g[i])>0:
						some_data.append(SeatingAndWritingSpace(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'pupils' : g[i],
	                                        }))
			try:
				SeatingAndWritingSpace.objects.bulk_create(some_data)
				messages.success(request, f'Pupils with adquate Seating and Writing Space by {year} have been recorded. Proceed to record Transfered Pupils')
				return redirect('add-transfered-students')
			except Exception:
				messages.warning(request, f'ERROR! May be Pupils with adquate Seating and Writing Space by {year} are already recorded. Only Fill the ones that are not yet recorded.')				
	else:
		student_form = SeatingAndWritingSpaceCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Seating and Writing Space',
	'student_form': student_form,
	'classes': classes,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_transfered_students(request):
	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)
	if request.method == 'POST':
		student_form = TransferedStudentCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, boys, girls]
			enrolment_list.append(std_records)
			for c, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(TransferedStudent(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				TransferedStudent.objects.bulk_create(some_data)
				messages.success(request, f'Transfers in {year} have been recorded. Proceed to record Pupils sitting Examinations.')
				return redirect('add-examinations')
			except Exception:
				messages.warning(request, f'ERROR! May be some Transfers in {year} are already recorded. Only Fill the ones that are not yet recorded.')				
	else:
		student_form = TransferedStudentCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Transfered Students',
	'student_form': student_form,
	'classes': classes,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_examinations(request):
	classes = None
	terms = Term.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	enrolment_list = []
	total_rows = len(classes)*len(terms)
	if request.method == 'POST':
		student_form = ExaminationCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			term = request.POST.getlist('term')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, term, boys, girls]
			enrolment_list.append(std_records)
			for c, a, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(Examination(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : Class.objects.get(pk=c[i]),
	                                        'term' : Term.objects.get(pk=a[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				Examination.objects.bulk_create(some_data)
				messages.success(request, f'Number of Pupils sitting Examinations each term in {year} have been recorded. View Students Registered')
				return redirect('view-students')
			except Exception:
				messages.warning(request, f'ERROR! May be some Pupils sitting Examinations each term in {year} are already recorded. Only Fill the ones that are not yet entered.')				
	else:
		student_form = ExaminationCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Examinations',
	'student_form': student_form,
	'classes': classes,
	'terms': terms,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_proposed_intake(request):
	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = IntakeClass.objects.filter(pk__lte=1)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = IntakeClass.objects.filter(pk__gte=2, pk__lte=2,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = IntakeClass.objects.filter(pk__gte=3, pk__lte=5,)
	else:
		classes = IntakeClass.objects.filter(pk__gt=5,)

	enrolment_list = []
	total_rows = len(classes)
	if request.method == 'POST':
		student_form = ProposedIntakeCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			class_name = request.POST.getlist('class_name')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [class_name, boys, girls]
			enrolment_list.append(std_records)
			for c, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(ProposedIntake(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'class_name' : IntakeClass.objects.get(pk=c[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				ProposedIntake.objects.bulk_create(some_data)
				messages.success(request, f'Proposed Intake for {year} have been recorded. Proceed to record Physical Streams.')
				return redirect('add-physical-streams')
			except Exception:
				messages.warning(request, f'ERROR! May be Proposed Intake of {year} are already recorded. Only Fill the ones that are not yet recorded.')				
	else:
		student_form = ProposedIntakeCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'Proposed Intake',
	'student_form': student_form,
	'classes': classes,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def add_new_entrants(request):
	ages = None
	if(request.user.schoolprofile.school.level_id==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(request.user.schoolprofile.school.level_id==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=20,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)

	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.get(pk=1)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.get(pk=4)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.get(pk=11)
	else:
		classes = Class.objects.get(pk=17)

	enrolment_list = []
	total_rows = len(ages)
	if request.method == 'POST':
		student_form = NewEntrantCreateForm(request.POST, )
		if student_form.is_valid():
			year = student_form.cleaned_data.get('year')
			age = request.POST.getlist('age')
			girls = request.POST.getlist('girls')
			boys = request.POST.getlist('boys')
			std_records = [age, boys, girls]
			enrolment_list.append(std_records)
			for c, g, b in enrolment_list:
				some_data = []
				for i in range(0, total_rows):
					if g[i]=='':
						g[i]=0
					if b[i]=='':
						b[i]=0
					if int(g[i])>0 or int(b[i])>0:
						some_data.append(NewEntrant(**{
	                                        'year' : year,
	                                        'user' : request.user,
	                                        'school' : request.user.schoolprofile.school,
	                                        'age' : AgeGroup.objects.get(pk=c[i]),
	                                        'girls' : g[i],
	                                        'boys' : b[i],
	                                        }))
			try:
				NewEntrant.objects.bulk_create(some_data)
				messages.success(request, f'New Entrants for {year} have been recorded. Proceed to record Pupils with adquate Seating and Writing Space.')
				return redirect('add-seating-and-writing-space')
			except Exception:
				messages.warning(request, f'ERROR! May be New Entrants of {year} are already recorded. Only Fill the ones that are not yet recorded.')				
	else:
		student_form = NewEntrantCreateForm()
	context = {
	'title': 'Students',
	'sub_title': 'New Entrants',
	'student_form': student_form,
	'ages': ages,
	'classes': classes,
	}
	return render(request, 'school/add_students.html', context)

@login_required
def view_students(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Student.objects.filter(school=request.user.schoolprofile.school, year=year).order_by('age_id',)
	students_by_class = Student.objects.values('class_name').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_age = Student.objects.values('age').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Student.objects.filter(school=request.user.schoolprofile.school, 
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
	'sub_title': 'Enrolment',
	'students': students,
	'classes': classes,
	'ages': ages,
	'students_by_class': students_by_class,
	'students_by_age': students_by_age,
	'total_students': total_students,
	'year':year
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_repeaters(request):
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Repeater.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_class = Repeater.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Repeaters',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_nationality(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Nationality.objects.filter(school=request.user.schoolprofile.school, year=year).order_by('country_id',)
	students_by_class = Nationality.objects.values('class_name').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_country = Nationality.objects.values('country').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Nationality.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	countries = Country.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Nationality',
	'students': students,
	'classes': classes,
	'countries': countries,
	'students_by_class': students_by_class,
	'students_by_country': students_by_country,
	'total_students': total_students,
	'year':year
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_proposed_intake(request):
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = ProposedIntake.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_class = ProposedIntake.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	if(request.user.schoolprofile.school.level_id==1):
		classes = IntakeClass.objects.filter(pk__lte=1)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = IntakeClass.objects.filter(pk__gte=2, pk__lte=2,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = IntakeClass.objects.filter(pk__gte=3, pk__lte=5,)
	else:
		classes = IntakeClass.objects.filter(pk__gt=5,)

	context = {
	'title': 'Students',
	'sub_title': 'Proposed Intake',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_physical_streams(request):
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = PhysicalStream.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_stream = PhysicalStream.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_streams=Sum('streams'))
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Physical Streams',
	'classes': classes,
	'students': students,
	'students_by_stream': students_by_stream,
	'year': year,
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_orphans(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Orphan.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_class = Orphan.objects.values('class_name').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_status = Orphan.objects.values('status').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = Orphan.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	statuses = OrphanStatus.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Orphans',
	'students': students,
	'classes': classes,
	'statuses': statuses,
	'students_by_class': students_by_class,
	'students_by_status': students_by_status,
	'total_students': total_students,
	'year':year
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_special_needs(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = SpecialNeed.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_class = SpecialNeed.objects.values('class_name').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	students_by_status = SpecialNeed.objects.values('status').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	total_students = SpecialNeed.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	statuses = SpecialNeedStatus.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Special Needs',
	'students': students,
	'classes': classes,
	'statuses': statuses,
	'students_by_class': students_by_class,
	'students_by_status': students_by_status,
	'total_students': total_students,
	'year':year
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_new_entrants(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = NewEntrant.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_age = NewEntrant.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	ages = None
	if(request.user.schoolprofile.school.level_id==1):
		ages = AgeGroup.objects.filter(pk__lte=4)
	elif(request.user.schoolprofile.school.level_id==2):
		ages = AgeGroup.objects.filter(pk__gte=5, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		ages = AgeGroup.objects.filter(pk__gte=13, pk__lte=20,)
	else:
		ages = AgeGroup.objects.filter(pk__gt=22,)

	classes = None
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.get(pk=1)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.get(pk=4)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.get(pk=11)
	else:
		classes = Class.objects.get(pk=17)

	context = {
	'title': 'Students',
	'sub_title': 'New Entrants',
	'classes': classes,
	'ages': ages,
	'students': students,
	'students_by_age': students_by_age,
	'year': year,
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_seating_and_writing_space(request):
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = SeatingAndWritingSpace.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_class = SeatingAndWritingSpace.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_pupils=Sum('pupils'))
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Seating and Writing Space',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_transfered_students(request):
	classes = None
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = TransferedStudent.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_class = TransferedStudent.objects.filter(school=request.user.schoolprofile.school, 
		year=year).aggregate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Transfered Students',
	'classes': classes,
	'students': students,
	'students_by_class': students_by_class,
	'year': year,
	}
	return render(request, 'school/view_students.html', context)

@login_required
def view_examinations(request):
	year=datetime.datetime.now().year
	if request.GET.get('year', None):
		year=request.GET.get('year', None)
	students = Examination.objects.filter(school=request.user.schoolprofile.school, year=year)
	students_by_term = Examination.objects.values('term').filter(school=request.user.schoolprofile.school, 
		year=year).annotate(total_girls=Sum('girls'), total_boys=Sum('boys'))
	classes = None
	terms = Term.objects.all()
	if(request.user.schoolprofile.school.level_id==1):
		classes = Class.objects.filter(pk__lte=3)
	elif(request.user.schoolprofile.school.level_id==2):
		classes = Class.objects.filter(pk__gte=4, pk__lte=10,)
	elif(request.user.schoolprofile.school.level_id==3):
		classes = Class.objects.filter(pk__gte=11, pk__lte=16,)
	else:
		classes = Class.objects.filter(pk__gt=16,)

	context = {
	'title': 'Students',
	'sub_title': 'Examinations',
	'students': students,
	'classes': classes,
	'terms': terms,
	'students_by_term': students_by_term,
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