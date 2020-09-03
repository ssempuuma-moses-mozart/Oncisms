import io
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from users.models import *
import datetime
import csv
def current_year():
    return datetime.date.today().year

def year_choices():
	return [(r,r) for r in range(1200, datetime.date.today().year+1)]

class SchoolCreateForm(forms.ModelForm):
	# yr_est = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, label="Year Established")
	# yr_reg = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, label="Year of Registration")
	# yr_cnr = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, label="Year of Center No. Registration")
	class Meta:
		model = School
		fields =('name','motto','phone','website','email','box_no','parish','address','fax','service_code','yr_est',
			'regstatus','reg_no','cen_no','level','highest_class','access','category','section','founder',
			'funder','operation_status','distance_to_nearest_school','distance_to_deo_office','logo')

class TeacherCreateForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields =('surname','first_name','payroll_number','education','profession','email','phone',
			'first_posting','first_appointment','responsibilities','gender','dob','nin',
			'salary_scale','on_payroll','training','previous_post','specialization','taught',
			'district','photo')

class TeacherTransferForm(forms.ModelForm):
	class Meta:
		model = TransferTeacher
		fields =('teacher','school','date_transfered','date_valid','designation')

class UploadDistrict(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)

		for record in reader:
			region = None
			if record['region'] != '':
				region = Region.objects.get(reg_name = (record['region']))
			else:
				region = Region.objects.get(pk = 1)
			District.objects.create(dis_name=record['dis_name'], region=region )

class UploadCounty(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)

		for record in reader:
			County.objects.create(county_name=record['county'],)

class UploadSubCounty(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)

		for record in reader:
			SubCounty.objects.create(subcounty_name=record['subcounty'],)

class UploadParish(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)

		for record in reader:
			district = None
			county = None
			subcounty = None
			if record['district'] != '':
				district = District.objects.get(dis_name = (record['district']))
			else:
				district = District.objects.get(pk = 1)
			if record['county'] != '':
				county = County.objects.get(county_name = (record['county']))
			else:
				county = County.objects.get(pk = 1)

			if record['subcounty'] != '':
				subcounty = SubCounty.objects.get(subcounty_name = (record['subcounty']))
			else:
				subcounty = SubCounty.objects.get(pk = 1)
			Parish.objects.create(parish_name=record['parish'], district=district, county=county, subcounty=subcounty )

# class UploadSchool(forms.Form):
# 	data_file = forms.FileField()

# 	def process_data(self):
# 		# with open(self.cleaned_data['data_file'].file, 'rb') as f:
# 		# 	reader = f.read()
# 		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
# 		reader = csv.DictReader(f)

# 		for record in reader:
# 			ownership = None
# 			district = None
# 			if record['ownership'] != '':
# 				ownership = Ownership.objects.get(own_type = (record['ownership']))
# 			else:
# 				ownership = Ownership.objects.get(pk = 1)

# 			if record['district'] != '':
# 				district = District.objects.get(dis_name = (record['district']))
# 			else:
# 				district = District.objects.get(pk = 1)

# 			level = Level.objects.get(pk = 2)
# 			School.objects.create(name=record['name'], ownership=ownership, district=district, level=level )

class UploadSchool(forms.Form):
	data_file = forms.FileField()

	def process_data(self):
		# with open(self.cleaned_data['data_file'].file, 'rb') as f:
		# 	reader = f.read()
		f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
		reader = csv.DictReader(f)

		for record in reader:
			parish = None
			level = None
			category = None
			section = None
			schtype = None

			if record['parish'] != '':
				parish = Parish.objects.get(parish_name = (record['parish']), 
					subcounty__subcounty_name = record.get('subcounty'),
					county__county_name = record.get('county'),)
			else:
				parish = Parish.objects.get(pk = 1)

			if record['level'] != '':
				level = Level.objects.get(lev_name = (record['level']))
			else:
				level = Level.objects.get(pk = 2)

			if record['category'] != '':
				category = Category.objects.get(cat_type = (record['category']))
			else:
				category = Category.objects.get(pk = 3)

			if record['section'] != '':
				section = Section.objects.get(sec_type = (record['section']))
			else:
				section = Section.objects.get(pk = 3)

			if record['operation_status'] != '':
				operation_status = Schtype.objects.get(sch_type = (record['operation_status']))
			else:
				operation_status = Schtype.objects.get(pk = 1)
			School.objects.create(name=record['name'], phone=record['phone'], parish=parish, level=level, category=category, 
				section=section, operation_status=operation_status )