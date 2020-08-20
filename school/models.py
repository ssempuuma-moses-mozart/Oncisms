from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ministry.models import * 
from users.models import *
class OnPayroll(models.Model):
	payroll = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.payroll

class AgeGroup(models.Model):
	value = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.value

class IntakeClass(models.Model):
	name = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.name

class Term(models.Model):
	term_name = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.term_name

class SchoolTeacherStatus(models.Model):
	status = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.status

class OrphanStatus(models.Model):
	status = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.status

class SpecialNeedStatus(models.Model):
	status = models.CharField(max_length=200, unique=True)
	def __str__(self):
		return self.status


class SchoolTeacher(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	on_payroll = models.ForeignKey(OnPayroll, default=1, on_delete=models.SET_DEFAULT)
	status = models.ForeignKey(SchoolTeacherStatus, default=1, on_delete=models.SET_DEFAULT)
	year_since = models.DateField()
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.teacher.name}'

class SchoolResource(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	amount = models.IntegerField()
	year = models.DateField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.resource.description}'

class Student(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	age = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','age','year',]

class Repeater(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year',]

class Nationality(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	country = models.ForeignKey(Country, default=1, on_delete=models.SET_DEFAULT)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year','country',]

class ProposedIntake(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(IntakeClass, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year',]

class PhysicalStream(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	year = models.IntegerField()
	streams = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year',]

class Orphan(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	status = models.ForeignKey(OrphanStatus, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year} {self.status}'

	class Meta():
		unique_together=['school','class_name','year','status',]

class SpecialNeed(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	status = models.ForeignKey(SpecialNeedStatus, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year} {self.status}'

	class Meta():
		unique_together=['school','class_name','year','status',]

class NewEntrant(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	age = models.ForeignKey(AgeGroup, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.age} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','age','year',]

class SeatingAndWritingSpace(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	year = models.IntegerField()
	pupils = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year',]

class TransferedStudent(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year',]

class Examination(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
	term = models.ForeignKey(Term, on_delete=models.CASCADE)
	girls = models.IntegerField(blank=True)
	boys = models.IntegerField(blank=True)
	year = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.class_name} {self.school.name} {self.year}'

	class Meta():
		unique_together=['school','class_name','year',]

class RequestStatus(models.Model):
	status = models.CharField(max_length=45)
	def __str__(self):
		return self.status
		
class RequestTeacher(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
	level = models.ForeignKey(Level, on_delete = models.CASCADE)
	comment = models.TextField()
	status = models.ForeignKey(RequestStatus, default=1, on_delete = models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.school.name} {self.subject}'

class RequestResource(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL)
	school = models.ForeignKey(School, on_delete=models.CASCADE)
	resource = models.ForeignKey(Resource, on_delete = models.CASCADE)
	reason = models.TextField()
	comment = models.TextField()
	status = models.ForeignKey(RequestStatus, default=1, on_delete = models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.school.name} {self.subject}'

