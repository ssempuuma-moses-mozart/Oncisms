from django.urls import path
from django.conf.urls import url
from . import views
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='website-home'),
    path('schools/<int:pk>/', views.schools, name='website-schools'),
    path('school/<int:pk>/', views.school, name='school'),
    path('school_levels/<int:pk>/', views.school_levels, name='school-levels'),
    path('teachers/', views.teachers, name='website-teachers'),
    path('DEOs/', views.deos, name='website-deos'),
    path('results/', views.results, name='website-results'),
    path('marketing/', views.marketing, name='website-marketing'),
    path('service_providers/<int:pk>/', views.service_providers, name='service-providers'),
    path('apply/', views.apply, name='apply'),
    path('covid19/', views.covid19, name='covid19'),
    path('covid19_downloads/<int:pk>/', views.covid19_downloads, name='covid19-downloads'),
    path('communication/', views.communication, name='website-communication'),
    path('resources/', views.resources, name='website-resources'),
    path('settings/', views.settings, name='website-settings'),
    path('slider/', SliderTemplate.as_view(), name='slider'),
    path('slider_main/', SliderMainTemplate.as_view(), name='slider-main'),

]
