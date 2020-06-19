from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from users.models import *
import datetime
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