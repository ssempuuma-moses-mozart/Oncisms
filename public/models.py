from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Service(models.Model):
	name = models.CharField(max_length=45, unique=True, verbose_name="Service Name")
	def __str__(self):
		return self.name

class Status(models.Model):
	name = models.CharField(max_length=45, unique=True, verbose_name="Application Status")
	def __str__(self):
		return self.name

class Classe(models.Model):
	name = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField(max_length=45, unique=True,)
	def __str__(self):
		return self.name

class ServiceProvider(models.Model):
	name = models.CharField(max_length=250, verbose_name="Service Provider Name")
	capacity = models.CharField(max_length=250, blank=True, null=True,)
	address = models.CharField(max_length=250, blank=True, null=True,)
	phone = models.CharField(max_length=13,)
	email = models.CharField(max_length=30,)
	description = models.TextField(blank=True, null=True,)
	service = models.ForeignKey(Service, on_delete = models.CASCADE)
	status = models.ForeignKey(Status, default=1, on_delete = models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.name

	class Meta():
		unique_together=['service','email',]

class LockdownPackage(models.Model):
	subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, blank=True, null=True,)
	topic = models.CharField(max_length = 200, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, )
	home_class = models.ForeignKey(Classe, on_delete = models.CASCADE, verbose_name="Package Work Class")
	home_work = models.FileField(upload_to="lockdown_package")	
	def __str__(self):
		return f'{self.home_class} {self.subject} {self.topic}'