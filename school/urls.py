from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='school-home'),
    path('profile/', views.profile, name='school-profile'),
    path('teacher/', views.teachers, name='school-teachers'),
    path('resource/', views.resources, name='school-resources'),
    path('set_profile/', SetProfileCreateView.as_view(), name='set-school-profile'),
    path('add_profile/', SchoolCreateView.as_view(), name='add-school-profile'),
    path('add_teacher/', SchoolTeacherCreateView.as_view(), name='add-school-teacher'),
    path('register_teacher/', TeacherCreateView.as_view(), name='register-teacher'),
    path('view_teachers/', SchoolTeacherListView.as_view(), name='view-school-teachers'),
    path('profile/<int:pk>/update/', SchoolUpdateView.as_view(), name='update-school-profile'),
    path('teacher/<int:pk>/update/', SchoolTeacherUpdateView.as_view(), name='update-school-teacher'),
    path('teacher/<int:pk>/', SchoolTeacherDetailView.as_view(), name='school-teacher-details'),
    path('add_resource/', SchoolResourceCreateView.as_view(), name='add-school-resource'),
    path('resource/<int:pk>/update/', SchoolResourceUpdateView.as_view(), name='update-school-resource'),
    path('view_resources/', SchoolResourceListView.as_view(), name='view-school-resources'),
    path('resource/<int:pk>/', SchoolResourceDetailView.as_view(), name='school-resource-details'),
    path('student/', views.students, name='students'),
    path('add_students/', StudentCreateView.as_view(), name='add-students'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='update-student'),
    path('view_students/', StudentListView.as_view(), name='view-students'),
    path('request_teacher/', RequestTeacherCreateView.as_view(), name='request-teacher'),
    path('request_teacher/<int:pk>/update/', RequestTeacherUpdateView.as_view(), name='update-teacher-request'),
    path('request_teacher/view/', RequestTeacherListView.as_view(), name='teacher-requests'),
]

