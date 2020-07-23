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
	yr_est = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, label="Year Established")
	yr_reg = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, label="Year of Registration")
	yr_cnr = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year, label="Year of Center No. Registration")
	class Meta:
		model = School
		fields =('name','motto','email','yr_est','regstatus','reg_no','yr_reg','cen_no',
			'cennostatus','yr_cnr','schtype','level','access','category','section',
			'ownership','district','logo')

class TeacherCreateForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields =('name','reg_no','date_registered','email','status','gender','dob','district','school','photo')

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