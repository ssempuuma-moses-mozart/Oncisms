from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ministry.models import * 
from users.models import *
class OnPayroll(models.Model):
	payroll = models.CharField(max_length=200)

	def __str__(self):
		return self.payroll

class SchoolTeacherStatus(models.Model):
	status = models.CharField(max_length=200)

	def __str__(self):
		return self.status
class SchoolTeacher(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	on_payroll = models.ForeignKey(OnPayroll, default=1, on_delete=models.SET_DEFAULT)
	status = models.ForeignKey(SchoolTeacherStatus, default=1, on_delete=models.SET_DEFAULT)
	year_since = models.DateField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.teacher.name}'

class SchoolResource(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	amount = models.IntegerField()
	year = models.DateField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.resource.description}'

class Class(models.Model):
	class_name = models.CharField(max_length=45, unique=True)

	def __str__(self):
		return self.class_name

class Student(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	no_of_students = models.IntegerField()
	year = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name}'

class Subject(models.Model):
	subject_name = models.CharField(max_length=45)
	subject_code = models.CharField(max_length=45)
	def __str__(self):
		return f'{self.subject_code} {self.subject_name}'

class RequestStatus(models.Model):
	status = models.CharField(max_length=45)
	def __str__(self):
		return self.status
		
class RequestTeacher(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
	level = models.ForeignKey(Level, on_delete = models.CASCADE)
	comment = models.TextField()
	status = models.ForeignKey(RequestStatus, default=1, on_delete = models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.user} {self.subject}'

class RequestResource(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	resource = models.ForeignKey(Resource, on_delete = models.CASCADE)
	reason = models.TextField()
	comment = models.TextField()
	status = models.ForeignKey(RequestStatus, default=1, on_delete = models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.user} {self.subject}'