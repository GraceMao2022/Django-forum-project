from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
                                      DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, \
                                        PermissionRequiredMixin
from django.template.defaultfilters import slugify
from django.apps import apps
from django.db.models import Count
from students.forms import CourseEnrollForm

from .models import Course, Subject

import string, random
 
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
 
def unique_slug_generator(Klass, title, new_slug = None):
    """ Generate a unique slug"""
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(title)
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug = slug).exists()
     
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug[:max_length-5], randstr = random_string_generator(size = 4))
        return unique_slug_generator(Klass, title, new_slug = new_slug)
    return slug

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                        LoginRequiredMixin,
                        PermissionRequiredMixin
                        ):
    model = Course
    fields = ['subject', 'title', 'overview']
    success_url = reverse_lazy('manage_course_list')

    def form_valid(self, form):
        form.instance.slug = unique_slug_generator(Course, form.instance.title)
        return super().form_valid(form)


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'
  

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/subjectlist.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.order_by('title').annotate(
                        total_courses=Count('courses'))
        # all_courses = Course.objects.annotate(
                            # total_modules=Count('modules'))
        all_courses = Course.objects.order_by('title')
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = all_courses.filter(subject=subject)
        else:
            courses = all_courses
        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
                                    initial={'course':self.object})
        context['enrolled'] = self.object.students.filter(pk= self.request.user.pk).exists()
        return context

class HomeView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request):
        return self.render_to_response({})
