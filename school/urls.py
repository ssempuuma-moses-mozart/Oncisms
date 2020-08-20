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
    path('add_students/enrolments/', views.add_students, name='add-students'),
    path('add_students/repeaters/', views.add_repeaters, name='add-repeaters'),
    path('view_students/repeaters/', views.view_repeaters, name='view-repeaters'),
    path('add_students/nationality/', views.add_nationality, name='add-nationality'),
    path('view_students/nationality/', views.view_nationality, name='view-nationality'),
    path('add_students/physical_streams/', views.add_physical_streams, name='add-physical-streams'),
    path('view_students/physical_streams/', views.view_physical_streams, name='view-physical-streams'),
    path('add_students/orphans/', views.add_orphans, name='add-orphans'),
    path('view_students/orphans/', views.view_orphans, name='view-orphans'),
    path('add_students/special_needs/', views.add_special_needs, name='add-special-needs'),
    path('view_students/special_needs/', views.view_special_needs, name='view-special-needs'),
    path('add_students/seating_and_writing_space/', views.add_seating_and_writing_space, name='add-seating-and-writing-space'),
    path('view_students/seating_and_writing_space/', views.view_seating_and_writing_space, name='view-seating-and-writing-space'),
    path('add_students/transfered_students/', views.add_transfered_students, name='add-transfered-students'),
    path('view_students/transfered_students/', views.view_transfered_students, name='view-transfered-students'),
    path('add_students/examinations/', views.add_examinations, name='add-examinations'),
    path('view_students/examinations/', views.view_examinations, name='view-examinations'),
    path('add_students/proposed_intake/', views.add_proposed_intake, name='add-proposed-intake'),
    path('view_students/proposed_intake/', views.view_proposed_intake, name='view-proposed-intake'),
    path('add_students/new_entrants/', views.add_new_entrants, name='add-new-entrants'),
    path('view_students/new_entrants/', views.view_new_entrants, name='view-new-entrants'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='update-student'),
    path('view_students/enrolments/', views.view_students, name='view-students'),
    path('request_teacher/', RequestTeacherCreateView.as_view(), name='request-teacher'),
    path('request_teacher/<int:pk>/update/', RequestTeacherUpdateView.as_view(), name='update-teacher-request'),
    path('request_teacher/view/', RequestTeacherListView.as_view(), name='teacher-requests'),
]

