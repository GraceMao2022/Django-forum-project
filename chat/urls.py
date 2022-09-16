from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'chat'

urlpatterns = [
    path('room/<int:course_id>/', views.course_qa_room, name='course_qa_room'),
    path('room/<int:course_id>/newquestion/', views.newQuestionPage, name='newquestion'),
    path('room/<int:course_id>/question/<str:question_id>/', views.questionPage, name='question'),
    path('room/<int:course_id>/updatenewquestion/<str:question_id>/', views.updatenewQuestionPage, name='updatenewquestion'),
    path('room/<int:course_id>/updatequestion/<str:question_id>/<str:response_id>/', views.updatequestionPage, name='updatequestion'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
