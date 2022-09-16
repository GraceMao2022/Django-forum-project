from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string



class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)
    # use a simple many-to-many instead of an intermediate model to have one less model to manage
    # but we need to delete a user from this relationship if we delete them from the course
    # https://docs.djangoproject.com/en/1.11/topics/db/models/#intermediary-manytomany
    email_notif_tutors = models.ManyToManyField(User,
                                      related_name='courses_monitored',
                                      blank=True)
    
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    
