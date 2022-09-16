from django.contrib import admin
from .models import Subject, Course

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created', 'owner']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview', 'owner']
    prepopulated_fields = {'slug': ('title',)}

######################################################################################




