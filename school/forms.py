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

class StudentCreateForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year,)
	class Meta:
		model = Student
		fields =('class_name','age','girls','boys','year')