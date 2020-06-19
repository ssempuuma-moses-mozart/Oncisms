from django.contrib import admin
from .models import *
from django.db import models
admin.site.register( SchoolTeacher )
admin.site.register( SchoolResource )
admin.site.register( SchoolTeacherStatus )
admin.site.register( OnPayroll )
admin.site.register( Class )
admin.site.register( Student )
admin.site.register( Subject )
admin.site.register( RequestTeacher )
admin.site.register( RequestStatus )
