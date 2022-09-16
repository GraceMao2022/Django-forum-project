from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import NewQuestionForm, NewResponseForm, EmailNotifForm
from django.http import HttpResponseForbidden
from django.core.mail import EmailMessage, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count

@login_required
def course_qa_room(request, course_id):
    course = None
    try:
        # retrieve course  with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()
    questions = course.questions.order_by('-created_at').annotate(total_responses=Count('responses'))
    email_notif = course.email_notif_tutors.filter(id=request.user.id).exists()
    is_tutor = request.user.groups.filter(name='Tutor').exists()
    if not is_tutor and email_notif:
        course.email_notif_tutors.remove(request.user)
    form = EmailNotifForm(initial={'email_notif': email_notif})
    context = {'questions': questions, 
               'course': course,
               'form': form,
               }

    if request.method == 'POST':
        try:
            form = EmailNotifForm(data=request.POST)
            if form.is_valid():
                email_notif_new = form.cleaned_data['email_notif']
                if not email_notif and email_notif_new:
                    course.email_notif_tutors.add(request.user)
                elif email_notif and not email_notif_new:
                    course.email_notif_tutors.remove(request.user)
            context['form'] = form
                
        except Exception as e:
            print(e)
            raise

    return render(request, 'chat/room.html', context)


@login_required
def newQuestionPage(request, course_id):
    form = NewQuestionForm()
    try:
        # retrieve course  with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        try:
            form = NewQuestionForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.course = course
                question.save()
                sendEmailNotif_question(request, question, course)
                return redirect('chat:course_qa_room', course_id)
        except Exception as e:
            print(e)
            raise

    context = {'form': form,
                'course': course}
    return render(request, 'chat/newquestion.html', context)

@login_required
def questionPage(request, course_id, question_id):
    response_form = NewResponseForm()
    try:
        # retrieve course  with given id joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except:
        # user is not a student of the course or course does not exist
        return HttpResponseForbidden()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(data=request.POST, files=request.FILES)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question.objects.get(id=question_id)
                response.save()
                sendEmailNotif_response(request, response, course)
                return redirect('chat:question', course_id , question_id)
        except Exception as e:
            print(e)
            raise
    question = Question.objects.get(id=question_id)
    context = {
        'course': course,
        'question': question,
        'response_form': response_form,
    }
    return render(request, 'chat/question.html', context)


def sendEmailNotif_question(request, question, course):
    
    messages = []
    current_site = get_current_site(request)


    for tutor in course.email_notif_tutors.all():
        message = render_to_string('chat/notification_email/new_question.html', {
            'tutor': tutor,
            'course': course,
            'question': question,
            'scheme': request.scheme,
            'domain': current_site.domain,
        })

        email_msg = (
            'New Question on MVHS SBS Forum',
            message,
            settings.EMAIL_HOST_USER,
            [tutor.email]
        )
        messages.append(email_msg)

    if messages:
        send_mass_mail(messages, fail_silently=False)


def sendEmailNotif_response(request, response, course):
    
    question = response.question
    question_author = question.author
    if(question_author.profile.receive_response_notif == False): 
        return

    # Skip if the question was asked by myself
    if response.user.id == question_author.id:
        return

    current_site = get_current_site(request)

    message = render_to_string('chat/notification_email/new_response.html', {
        'course': course,
        'question': question,
        'scheme': request.scheme,
        'domain': current_site.domain,
    })

    email = EmailMessage(''
        'New Response on MVHS SBS Forum',
        message,
        settings.EMAIL_HOST_USER,
        [question_author.email]
    )

    email.fail_silently=False
    email.send()

@login_required
def updatenewQuestionPage(request, course_id, question_id):
    question=Question.objects.get(id=question_id)
    form = NewQuestionForm(instance=question)
    course = request.user.courses_joined.get(id=course_id)
    if request.user == question.author:
        if request.method == 'POST':
            try:
                form = NewQuestionForm(request.POST, files=request.FILES, instance=question)
                if form.is_valid():
                    question = form.save(commit=False)
                    question.save()
                    return redirect( 'chat:question', course_id , question_id)
            except Exception as e:
                print(e)
                raise
        context = {'form': form,
                    'course': course}
        return render(request, 'chat/newquestion.html', context)
    else:
         return HttpResponseForbidden()

@login_required
def updatequestionPage(request, course_id, question_id, response_id):
    question = Question.objects.get(id=question_id)
    response = Response.objects.get(id=response_id)
    response_form = NewResponseForm(instance=response)
    course = request.user.courses_joined.get(id=course_id)
    if request.user == response.user:
        if request.method == 'POST':
            try:
                response_form = NewResponseForm(request.POST, files=request.FILES, instance=response)
                if response_form.is_valid():
                    response = response_form.save(commit=False)
                    response.user = request.user
                    response.question = Question.objects.get(id=question_id)
                    response.save()
                    return redirect('chat:question', course_id , question_id)
            except Exception as e:
                print(e)
                raise
        context = {
            'course': course,
            'question': question,
            'response': response,
            'response_form': response_form,
        }
        return render(request, 'chat/question.html', context)

    else:
        return HttpResponseForbidden()
