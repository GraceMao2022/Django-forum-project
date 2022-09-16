from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from courses.models import Course
from .forms import CourseEnrollForm, UserRegisterForm

from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat:course_qa_room',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from students.forms import UserRegisterForm, ProfileForm
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from students.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.conf import settings

# Sign Up View
class SignUpView(View):
    form_class = UserRegisterForm
    template_name = 'students/student/registration.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('students/student/emails/account_activation_email.html', {
                'user': user,
                'scheme': request.scheme,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                'Activate Your MVHSForum Account',
                message,
                settings.EMAIL_HOST_USER,
                [user.email]
            )

            email.fail_silently=False
            email.send()

            return redirect('prompt', 'email-verification')

        return render(request, self.template_name, {'form': form})

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .forms import ProfileForm, SettingsForm
from django.forms.models import model_to_dict

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            return redirect('prompt', 'account-confirmed')
        else:
            return redirect('prompt', 'confirmation-invalid')


# Edit Profile View
class ProfileView(LoginRequiredMixin, View):
    template_name = 'students/student/profile.html'

    def get(self, request, *args, **kwargs):
        # profile = request.user.profile
        # form = ProfileForm(model_to_dict(profile))
        # context = {'profile': profile, 'form': form}
        return render(request, self.template_name, {})

class SettingsView(LoginRequiredMixin, View):
    template_name = 'students/student/settings.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = SettingsForm(model_to_dict(profile))
        context = {'profile': profile, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = SettingsForm(request.POST)
        if form.is_valid():
            tmp_profile = form.save(commit=False)
            profile.receive_response_notif = tmp_profile.receive_response_notif
            profile.save()
            return redirect('profile')

        context = {'profile': profile, 'form': form}
        return render(request, self.template_name, context)
    

# Display a message in a separate page
class PromptView(View):
    template_name = 'students/student/prompts.html'
    def get(self, request, prompt_type, *args, **kwargs):
        if prompt_type == 'email-verification':
            title = 'Email Verification'
            message = 'Your account has been created. An email has been sent to your email address for verification. Please confirm your email to complete registration.'
        elif prompt_type == 'account-confirmed':
            title = 'Account Confirmed'
            message = 'Your account has been confirmed.'
        elif prompt_type == 'confirmation-invalid':
            title = 'Confirmation Invalid'
            message = 'The confirmation link is invalid, possibly because it has already been used.'

        return render(request, self.template_name, {'title': title, 'message': message})
