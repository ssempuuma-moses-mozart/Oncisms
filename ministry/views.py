from django.shortcuts import render, redirect
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

from .models import *
from .forms import *
from school.models import *
from django.db import IntegrityError
from django.db.models import Sum


# class HomeView(DetailView):
# 	model = School
# 	template_name = "ministry/home.html"
# 	def get_context_data(self, **kwargs):
# 		context = super(HomeView, self).get_context_data(**kwargs)
# 		context['all_schools'] = School.objects.all().order_by('-id')
# 		all_regs = School.objects.values("region").annotate(Count("id"))
# 		context['all_resources'] = Resource.objects.all().order_by('-id')
# 		context['teachers'] = Teacher.objects.all().order_by('-id')[:10]
# 		context['deos'] = Deo.objects.all().order_by('-id')
# 		context['teacher_transfers'] = TransferTeacher.objects.all().order_by('-id')
# 		context['deo_transfers'] = TransferDeo.objects.all().order_by('-id')
# 		context['allocated_resources'] = AllocateResource.objects.all().order_by('-id')
		# return context

# School related views..................................................................................
# School related views..................................................................................

class SchoolListView(ListView):
	model = School
	def get_context_data(self, **kwargs):
		context = super(SchoolListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		schools = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["schools"] = schools.get_page(page)
		context["title"] = "Schools"
		return context

class SchoolDetailView(DetailView):
	model = School
	def get_context_data(self, **kwargs):
		context = super(SchoolDetailView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		schools = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["schools"] = schools.get_page(page)
		context["title"] = "Schools"
		return context

class SchoolCreateView(LoginRequiredMixin, CreateView):
	model = School
	template_name = "ministry/school_form.html"
	form_class = SchoolCreateForm
	def get_context_data(self, **kwargs):
		context = super(SchoolCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		schools = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["schools"] = schools.get_page(page)
		context["title"] = "Schools"
		return context

	def form_valid(self, form):
		form = SchoolCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-school')

class SchoolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = School
	template_name = "ministry/school_form.html"
	form_class = SchoolCreateForm
	def get_context_data(self, **kwargs):
		context = super(SchoolUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		schools = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["schools"] = schools.get_page(page)
		context["title"] = "Schools"
		return context

	def form_valid(self, form):
		school = School.objects.get(pk=self.object.id)
		form = SchoolCreateForm(self.request.POST, self.request.FILES, instance=school)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have updated {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-school')

# Teacher related views..................................................................................
# Teacher related views..................................................................................

class TeacherCreateView(LoginRequiredMixin, CreateView):
	model = Teacher
	form_class = TeacherCreateForm
	def get_context_data(self, **kwargs):
		context = super(TeacherCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		form = TeacherCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-teacher')

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
	form_class = TeacherCreateForm
	model = Teacher
	def get_context_data(self, **kwargs):
		context = super(TeacherUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		teacher = Teacher.objects.get(pk=self.object.id)
		form = TeacherCreateForm(self.request.POST, self.request.FILES, instance=teacher)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have updated {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('new-teacher')

class TeacherListView(ListView):
	model = Teacher
	def get_context_data(self, **kwargs):
		context = super(TeacherListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

class TeacherDetailView(DetailView):
	model = Teacher
	def get_context_data(self, **kwargs):
		context = super(TeacherDetailView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teachers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

class TeacherTransferListView(ListView):
	model = TransferTeacher
	def get_context_data(self, **kwargs):
		context = super(TeacherTransferListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["teacher_transfers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

class TransferTeacherCreateView(LoginRequiredMixin, CreateView):
	model = TransferTeacher
	form_class = TeacherTransferForm
	def get_context_data(self, **kwargs):
		context = super(TransferTeacherCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		teachers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["transfers"] = teachers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		form = TeacherTransferForm(self.request.POST, self.request.FILES,)
		if form.is_valid():
			form.instance.user = self.request.user
			form.save(commit=False)
			teacher = form.cleaned_data.get('teacher')
			form.instance.school_from = teacher.school
			try:
				form.save()
				teacher = form.cleaned_data.get('teacher')
				messages.success(self.request, f'Thank you! The Transfer of {teacher} was successful')
			except IntegrityError:
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('transfer-teacher')

class TransferTeacherUpdateView(LoginRequiredMixin, UpdateView):
	model = TransferTeacher
	form_class = TeacherTransferForm
	def get_context_data(self, **kwargs):
		context = super(TransferTeacherUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		transfers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["transfers"] = transfers.get_page(page)
		context["title"] = "Teachers"
		return context

	def form_valid(self, form):
		transfer = TransferTeacher.objects.get(pk=self.object.id)
		form = TeacherTransferForm(self.request.POST, self.request.FILES, instance=transfer)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('teacher')
				messages.success(self.request, f'Thank you! You have updated {name}`s transfer')
			except IntegrityError:
				name = form.cleaned_data.get('teacher')
				messages.warning(self.request, f'ERROR! Some thing went wrong. Try again')
			return redirect('transfer-teacher')


class DesignationCreateView(LoginRequiredMixin, CreateView):
	model = Designation
	fields =['des_type']
	def get_context_data(self, **kwargs):
		context = super(DesignationCreateView, self).get_context_data(**kwargs)
		context["des"] = self.model.objects.all().order_by('-id')
		return context

	def form_valid(self, form):
		form.save()
		return redirect('designation')

class DesignationUpdateView(LoginRequiredMixin, UpdateView):
	model = Designation
	fields =['des_type']
	def get_context_data(self, **kwargs):
		context = super(DesignationUpdateView, self).get_context_data(**kwargs)
		context["des"] = self.model.objects.all().order_by('-id')
		return context

	def form_valid(self, form):
		form.save()
		return redirect('designation')

# Deo related views..................................................................................
# Deo related views..................................................................................

class DeoCreateView(LoginRequiredMixin, CreateView):
	model = Deo
	fields =['name','email','status','gender','district','region','photo']
	def get_context_data(self, **kwargs):
		context = super(DeoCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deos = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deos"] = deos.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('new-deo')

class DeoUpdateView(LoginRequiredMixin, UpdateView):
	model = Deo
	fields =['name','email','status','gender','district','region','photo']
	def get_context_data(self, **kwargs):
		context = super(DeoUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deos = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deos"] = deos.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('new-deo')

class DeoListView(ListView):
	model = Deo
	context_object_name = 'deos'
	ordering = ['-id']

class DeoDetailView(DetailView):
	model = Deo
	def get_context_data(self, **kwargs):
		context = super(DeoDetailView, self).get_context_data(**kwargs)
		context['deotransfers'] = TransferDeo.objects.filter(deo=self.object)
		return context

class TransferDeoCreateView(LoginRequiredMixin, CreateView):
	model = TransferDeo
	fields =['deo','district','date_transfered','date_valid']
	def get_context_data(self, **kwargs):
		context = super(TransferDeoCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deotransfers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deotransfers"] = deotransfers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('transfer-deo')

class TransferDeoUpdateView(LoginRequiredMixin, UpdateView):
	model = TransferDeo
	fields =['deo','district','date_transfered','date_valid']
	def get_context_data(self, **kwargs):
		context = super(TransferDeoUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		deotransfers = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["deotransfers"] = deotransfers.get_page(page)
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return redirect('transfer-deo')

# Fac related views..................................................................................
# Fac related views..................................................................................

class FacilityCreateView(LoginRequiredMixin, CreateView):
	model = Facility
	fields =['facility_type','description','quantity','status','photo']
	template_name = "ministry/facility_form.html"
	def get_context_data(self, **kwargs):
		context = super(FacilityCreateView, self).get_context_data(**kwargs)
		context["facilities"] = self.model.objects.all().order_by('-id')
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		# form.instance.school = self.request.session.get['sch_id']
		form.save()
		return HttpResponseRedirect("")
		# return redirect('new-facility')

# School settings related views..................................................................................
# School settings views..................................................................................

class OwnershipCreateView(LoginRequiredMixin, CreateView):
	model = Ownership
	fields =['own_type']
	def get_context_data(self, **kwargs):
		context = super(OwnershipCreateView, self).get_context_data(**kwargs)
		context["own_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('ownership')

class OwnershipUpdateView(LoginRequiredMixin, UpdateView):
	model = Ownership
	fields =['own_type']
	def get_context_data(self, **kwargs):
		context = super(OwnershipUpdateView, self).get_context_data(**kwargs)
		context["own_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('ownership')

class SectionCreateView(LoginRequiredMixin, CreateView):
	model = Section
	fields =['sec_type']
	def get_context_data(self, **kwargs):
		context = super(SectionCreateView, self).get_context_data(**kwargs)
		context["sec_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('section')

class SectionUpdateView(LoginRequiredMixin, UpdateView):
	model = Section
	fields =['sec_type']
	def get_context_data(self, **kwargs):
		context = super(SectionUpdateView, self).get_context_data(**kwargs)
		context["sec_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('section')

class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	fields =['cat_type']
	def get_context_data(self, **kwargs):
		context = super(CategoryCreateView, self).get_context_data(**kwargs)
		context["cat_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('category')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	fields =['cat_type']
	def get_context_data(self, **kwargs):
		context = super(CategoryUpdateView, self).get_context_data(**kwargs)
		context["cat_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('category')

class LevelCreateView(LoginRequiredMixin, CreateView):
	model = Level
	fields =['lev_name']
	def get_context_data(self, **kwargs):
		context = super(LevelCreateView, self).get_context_data(**kwargs)
		context["levels"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('level')

class LevelUpdateView(LoginRequiredMixin, UpdateView):
	model = Level
	fields =['lev_name']
	def get_context_data(self, **kwargs):
		context = super(LevelUpdateView, self).get_context_data(**kwargs)
		context["levels"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('level')

class AccessCreateView(LoginRequiredMixin, CreateView):
	model = Access
	fields =['acc_type']
	def get_context_data(self, **kwargs):
		context = super(AccessCreateView, self).get_context_data(**kwargs)
		context["acc_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('access')

class AccessUpdateView(LoginRequiredMixin, UpdateView):
	model = Access
	fields =['acc_type']
	def get_context_data(self, **kwargs):
		context = super(AccessUpdateView, self).get_context_data(**kwargs)
		context["acc_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('access')

class RegstatusCreateView(LoginRequiredMixin, CreateView):
	model = Regstatus
	fields =['rs_type']
	def get_context_data(self, **kwargs):
		context = super(RegstatusCreateView, self).get_context_data(**kwargs)
		context["rs_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('regstatus')

class RegstatusUpdateView(LoginRequiredMixin, UpdateView):
	model = Regstatus
	fields =['rs_type']
	def get_context_data(self, **kwargs):
		context = super(RegstatusUpdateView, self).get_context_data(**kwargs)
		context["rs_types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('regstatus')

class CennostatusCreateView(LoginRequiredMixin, CreateView):
	model = Cennostatus
	fields =['cns']
	def get_context_data(self, **kwargs):
		context = super(CennostatusCreateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('cennostatus')

class CennostatusUpdateView(LoginRequiredMixin, UpdateView):
	model = Cennostatus
	fields =['cns']
	def get_context_data(self, **kwargs):
		context = super(CennostatusUpdateView, self).get_context_data(**kwargs)
		context["statuses"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('cennostatus')

class SchtypeCreateView(LoginRequiredMixin, CreateView):
	model = Schtype
	fields =['sch_type']
	def get_context_data(self, **kwargs):
		context = super(SchtypeCreateView, self).get_context_data(**kwargs)
		context["types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('schtype')

class SchtypeUpdateView(LoginRequiredMixin, UpdateView):
	model = Schtype
	fields =['sch_type']
	def get_context_data(self, **kwargs):
		context = super(SchtypeUpdateView, self).get_context_data(**kwargs)
		context["types"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('schtype')

class DistrictCreateView(LoginRequiredMixin, CreateView):
	model = District
	fields =['dis_name']
	def get_context_data(self, **kwargs):
		context = super(DistrictCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		districts = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["districts"] = districts.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('district')

class DistrictUpdateView(LoginRequiredMixin, UpdateView):
	model = District
	fields =['dis_name']
	def get_context_data(self, **kwargs):
		context = super(DistrictUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		districts = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["districts"] = districts.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('district')

class RegionCreateView(LoginRequiredMixin, CreateView):
	model = Region
	fields =['reg_name']
	def get_context_data(self, **kwargs):
		context = super(RegionCreateView, self).get_context_data(**kwargs)
		context["regions"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('region')

class RegionUpdateView(LoginRequiredMixin, UpdateView):
	model = Region
	fields =['reg_name']
	def get_context_data(self, **kwargs):
		context = super(RegionUpdateView, self).get_context_data(**kwargs)
		context["regions"] = self.model.objects.all().order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('region')

# Fac settings related views..................................................................................
# Fac settings related views..................................................................................

class FacilityTypeView(LoginRequiredMixin, CreateView):
    model = FacilityType
    fields =['facility_type']
    template_name = "ministry/facility_type_form.html"
    def get_context_data(self, **kwargs):
        context = super(FacilityTypeView, self).get_context_data(**kwargs)
        context["fac_types"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('factype')

class FacilityTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = FacilityType
    fields =['facility_type']
    template_name = "ministry/facility_type_form.html"
    def get_context_data(self, **kwargs):
        context = super(FacilityTypeUpdateView, self).get_context_data(**kwargs)
        context["fac_types"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('factype')

class FacilityStatusView(LoginRequiredMixin, CreateView):
    model = FacilityStatus
    fields =['facility_status']
    template_name = "ministry/facility_status_form.html"
    def get_context_data(self, **kwargs):
        context = super(FacilityStatusView, self).get_context_data(**kwargs)
        context["statuses"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('facstatus')
    	
class FacilityStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = FacilityStatus
    fields =['facility_status']
    template_name = "ministry/facility_status_form.html"
    def get_context_data(self, **kwargs):
        context = super(FacilityStatusUpdateView, self).get_context_data(**kwargs)
        context["statuses"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('facstatus')

class TeacherStatusCreateView(LoginRequiredMixin, CreateView):
    model = TeacherStatus
    fields =['teacher_status']
    def get_context_data(self, **kwargs):
        context = super(TeacherStatusCreateView, self).get_context_data(**kwargs)
        context["statuses"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('teacher-status')


# Teacher settings related views..................................................................................
# Teacher settings views..................................................................................

class TeacherStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = TeacherStatus
    fields =['teacher_status']
    def get_context_data(self, **kwargs):
        context = super(TeacherStatusUpdateView, self).get_context_data(**kwargs)
        context["statuses"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('teacher-status')

class GenderCreateView(LoginRequiredMixin, CreateView):
    model = Gender
    fields =['gender']
    def get_context_data(self, **kwargs):
        context = super(GenderCreateView, self).get_context_data(**kwargs)
        context["gender_types"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('gender')

class GenderUpdateView(LoginRequiredMixin, UpdateView):
    model = Gender
    fields =['gender']
    def get_context_data(self, **kwargs):
        context = super(GenderUpdateView, self).get_context_data(**kwargs)
        context["gender_types"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('gender')

# Resource related views..................................................................................
# Resource related views..................................................................................

class ResourceSourceCreateView(LoginRequiredMixin, CreateView):
	model = ResourceSource
	fields =['resource_source']
	def get_context_data(self, **kwargs):
		context = super(ResourceSourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resource_sources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resource_sources"] = resource_sources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('resource-source')

class ResourceSourceUpdateView(LoginRequiredMixin, UpdateView):
	model = ResourceSource
	fields =['resource_source']
	def get_context_data(self, **kwargs):
		context = super(ResourceSourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resource_sources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resource_sources"] = resource_sources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.save()
			return redirect('resource-source')

class ResourceListView(ListView):
	model = Resource
	def get_context_data(self, **kwargs):
		context = super(ResourceListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		context["title"] = "Resources"
		return context

class ResourceTypeCreateView(LoginRequiredMixin, CreateView):
    model = ResourceType
    fields =['resource_type']
    def get_context_data(self, **kwargs):
        context = super(ResourceTypeCreateView, self).get_context_data(**kwargs)
        context["resource_types"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('resource-type')

class ResourceTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = ResourceType
    fields =['resource_type']
    def get_context_data(self, **kwargs):
        context = super(ResourceTypeUpdateView, self).get_context_data(**kwargs)
        context["resource_types"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('resource-type')

class ResourceCreateView(LoginRequiredMixin, CreateView):
	model = Resource
	fields =['description','resource_type','source','quantity','amount','year','photo']
	def get_context_data(self, **kwargs):
		context = super(ResourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('resource')

class ResourceUpdateView(LoginRequiredMixin, UpdateView):
	model = Resource
	fields =['description','resource_type','source','quantity','amount','year','photo']
	def get_context_data(self, **kwargs):
		context = super(ResourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["resources"] = resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('resource')

class ResourceDetailView(DetailView):
	model = Resource
	def get_context_data(self, **kwargs):
		context = super(ResourceDetailView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocated = Paginator(AllocateResource.objects.filter(resource=self.object).order_by('-id'), 10)
		context["allocated"] = allocated.get_page(page)
		return context

class AllocateResourceCreateView(LoginRequiredMixin, CreateView):
	model = AllocateResource
	fields =['resource','school','quantity','amount','date_allocated','date_valid','year']
	def get_context_data(self, **kwargs):
		context = super(AllocateResourceCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocate_resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["allocate_resources"] = allocate_resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save(commit=False)
			resource = form.cleaned_data.get('resource')
			amount = form.cleaned_data.get('amount')
			qty = form.cleaned_data.get('quantity')
			amount_all = AllocateResource.objects.filter()
			return redirect('allocate-resource')

class AllocateResourceUpdateView(LoginRequiredMixin, UpdateView):
	model = AllocateResource
	fields =['resource','school','quantity','amount','date_allocated','date_valid','year']
	def get_context_data(self, **kwargs):
		context = super(AllocateResourceUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocate_resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["allocate_resources"] = allocate_resources.get_page(page)
		context["title"] = "Resources"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('allocate-resource')

class ResourceListView(ListView):
	model = Resource
	context_object_name = 'resources'
	ordering = ['-id']

class AllocateResourceListView(ListView):
	model = AllocateResource
	def get_context_data(self, **kwargs):
		context = super(AllocateResourceListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		allocate_resources = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["allocate_resources"] = allocate_resources.get_page(page)
		context["title"] = "Resources"
		return context

class ProductCreateView(LoginRequiredMixin, CreateView):
	model = Product
	fields =['title','description','price','phone_contact','photo']
	def get_context_data(self, **kwargs):
		context = super(ProductCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		products = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 10)
		context["products"] = products.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('product')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Product
	fields =['title','description','price','phone_contact','status','photo']
	def get_context_data(self, **kwargs):
		context = super(ProductUpdateView, self).get_context_data(**kwargs)
		context["products"] = self.model.objects.filter(user=self.request.user).order_by('-id')
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('product')
	def test_func(self):
		product = self.get_object()
		if self.request.user == product.user:
			return True
		return False

class ProductListView(ListView):
	model = Product
	context_object_name = 'products'
	ordering = ['-id']

class UserProducts(ListView):
	model = Product
	def get_context_data(self, **kwargs):
		context = super(UserProducts, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		products = pagenator = Paginator(self.model.objects.filter(user=self.request.user).order_by('-id'), 2)
		context["products"] = products.get_page(page)
		return context

class ProductDetailView(DetailView):
	model = Product

class ProductStatusCreateView(LoginRequiredMixin, CreateView):
    model = ProductStatus
    fields =['status']
    def get_context_data(self, **kwargs):
        context = super(ProductStatusCreateView, self).get_context_data(**kwargs)
        context["statuses"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('product-status')

class ProductStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductStatus
    fields =['status']
    def get_context_data(self, **kwargs):
        context = super(ProductStatusUpdateView, self).get_context_data(**kwargs)
        context["statuses"] = self.model.objects.all().order_by('-id')
        return context
    def form_valid(self, form):
    	if form.is_valid():
    		form.save()
    		return redirect('product-status')

class SubjectCreateView(LoginRequiredMixin, CreateView):
	model = Subject
	template_name = "ministry/subject_form.html"
	fields =['subject_code','subject_name']
	def get_context_data(self, **kwargs):
		context = super(SubjectCreateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		subjects = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["subjects"] = subjects.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('subject')

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
	model = Subject
	template_name = "ministry/subject_form.html"
	fields =['subject_code','subject_name']
	def get_context_data(self, **kwargs):
		context = super(SubjectUpdateView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		subjects = Paginator(self.model.objects.all().order_by('-id'), 10)
		context["subjects"] = subjects.get_page(page)
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			return redirect('subject')

def home(request):
	all_schools = School.objects.count()
	all_deos = Deo.objects.count()
	all_teachers = Teacher.objects.count()
	all_resources = Resource.objects.count()
	all_trtransfer = TransferTeacher.objects.count()
	all_deotransfer = TransferDeo.objects.count()
	return render(request, 'ministry/home.html', {'title': 'Home', 
		'all_schools':all_schools, 
		'all_deos':all_deos, 
		'all_teachers':all_teachers, 
		'all_resources':all_resources, 
		'all_trtransfer':all_trtransfer, 
		'all_deotransfer':all_deotransfer })

def schools(request):
	return render(request, 'ministry/schools.html', {'title': 'Schools'})

def teachers(request):
	return render(request, 'ministry/teachers.html', {'title': 'Teachers'})

def deos(request):
	return render(request, 'ministry/deos.html', {'title': 'DEOs'})

def resources(request):
	return render(request, 'ministry/resources.html', {'title': 'Resources'})

def marketing(request):
	product_list = Product.objects.filter(status=1).order_by('-id')
	products_sold = Product.objects.filter(user=request.user, status=2).order_by('-id')
	paginator = Paginator(product_list, 5)
	page = request.GET.get('page')
	products = paginator.get_page(page)
	return render(request, 'ministry/marketing.html', {'title': 'Marketing', 'products':products, 'products_sold':products_sold})

def communication(request):
	return render(request, 'ministry/communication.html', {'title': 'Communication'})

def settings(request):
	return render(request, 'ministry/settings.html', {'title': 'Settings'})