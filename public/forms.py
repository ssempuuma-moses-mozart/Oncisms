from django import forms
from .models import *
import datetime

class ApplyCreateForm(forms.ModelForm):
	class Meta:
		model = ServiceProvider
		fields =('service','name','capacity','phone','email','address','description')