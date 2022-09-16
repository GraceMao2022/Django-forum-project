from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from courses.models import Course


# Create your models here.
class Question(models.Model):  
    
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200, null=False)
    #body = RichTextField(blank=True, null=True)
    #body = models.TextField(null=False)
    body = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    masques = models.BooleanField(null=True)
    
    
    def __str__(self):
        return self.title

    def get_responses(self):
        return self.responses.filter(parent=None)

    
    

class Response(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='responses')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = RichTextUploadingField(blank=True, null=True)
    #body = RichTextField(blank=True, null=True)
    #body = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    masques = models.BooleanField(null=True)

    def __str__(self):
        return self.body

    def get_responses(self):
        return Response.objects.filter(parent=self)

