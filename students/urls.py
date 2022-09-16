# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 16:13:40 2021

@author: 
"""

from django.urls import path
from django.views.decorators.cache import cache_page
from . import views
from students.views import ProfileView, SettingsView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(),name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('prompt/<prompt_type>', views.PromptView.as_view(), name='prompt'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('enroll-course/',
          views.StudentEnrollCourseView.as_view(),
          name='student_enroll_course'),

    path('courses/',
          views.StudentCourseListView.as_view(),
          name='student_course_list'),
  
    # path('course/<pk>/',
    #      cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
    #      name='student_course_detail'),
    # path('course/<pk>/<module_id>/',
    #      cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
    #      name='student_course_detail_module'),

    # Change Password
    path('change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='students/student/change-password.html',
            success_url = '/students/change-password/done'
        ),
        name='change_password'
    ),   
    path('change-password/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='students/student/change-password-done.html'
         ),
         name='change_password_done'),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='students/student/password-reset/password_reset.html',
             subject_template_name='students/student/password-reset/password_reset_subject.txt',
             email_template_name='students/student/password-reset/password_reset_email.html',
             success_url='/students/password-reset/done'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='students/student/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='students/student/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='students/student/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
