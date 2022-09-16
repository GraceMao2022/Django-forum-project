from django.contrib import admin
from  .models import Question, Response

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'course']
    list_filter = ['created_at', 'course','author']
    search_fields = ['title']

    
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['question']
