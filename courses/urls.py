# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 22:30:08 2021

@author: 
"""

from django.urls import path
from . import views

urlpatterns = [
    path('mine/',
         views.ManageCourseListView.as_view(),
         name='manage_course_list'),

    path('create/',
         views.CourseCreateView.as_view(),
         name='course_create'),

    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),

    path('<pk>/delete/',
         views.CourseDeleteView.as_view(),
         name='course_delete'),
         
    path('subject/<slug:subject>/',
         views.CourseListView.as_view(),
         name='course_list_subject'),

     path('subjectlist/',
         views.CourseListView.as_view(),
         name='subject_list'),   
         
    path('<slug:slug>/',
         views.CourseDetailView.as_view(),
         name='course_detail'),   
  
]