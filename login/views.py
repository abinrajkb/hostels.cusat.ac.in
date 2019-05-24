import smtplib
import socket

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .models import VerifiedUser
from .forms import UserForm, OTP_resendform, LoginForm
from django.core.mail import send_mail
from django.conf import settings


class AuthenticationView(LoginView):
    template_name = 'login/login.html'
    form_class = LoginForm
    extra_context = {
        'form1': UserForm

    }
    redirect_authenticated_user = True

    def get_success_url(self):
        if not self.request.user.applications.Pincode:
            return "/apply/"
        return "/apply/view/"

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        print(request.POST)
        try:
            verifieduser = VerifiedUser.objects.get(username=request.POST['username'])
            if (verifieduser.is_active):
                return super().post(request, *args, **kwargs)

            context = {'error_heading': 'A Verification link has been sent to your email account',
                       'error_message': 'Please click on the link that has been sent to your email account to verify '
                                        '   your email and continue login again'}
        except VerifiedUser.DoesNotExist:

            context = {'error_heading': 'Seems like your are not registered yet',
                       'error_message': 'Please SignUp to continue'}
        return render(request, 'login/login.html', context=context)


def register(request):
    if request.method == 'POST':
        OTLink = make_password(request.POST['username'])
        context = {
            "form1": LoginForm,
            "login": 'Sign Up',
            'signup': 'Login',

        }
        user = UserForm(request.POST)
        if (user.is_valid()):
            user = user.save()

            if user.is_active:
                return HttpResponseRedirect('/apply/')
            else:
                context = {'error_heading': 'A Verification link has been sent to your email account',
                           'error_message': 'Please click on the link that has been sent to your email account to verify '
                                            '   your email and continue login again',
                           "resend": True}
                return render(request, 'login/login.html', context=context)

        else:
            context["form"] = user
            user.show_error = True
            return render(request, 'login/login.html', context=context)

    else:
        return HttpResponseRedirect("/auth/")


def verification(request, token):
    print(token)
    verifying_user = VerifiedUser.objects.get(userhash=token)
    verifying_user.is_active = True
    verifying_user.save()
    context = {
        'form1': UserForm,
        'form': LoginForm,
        'valid': "Successfully Verified . Login To Apply"
    }
    return render(request, 'login/login.html', context=context)


def resend_otp(request):
    context = {
        "form": OTP_resendform,
        "login": "Resend OTP"
    }
    if request.method == "POST":
        form = OTP_resendform(request)
        email = form["Email_Address"].value
        try:
            print(email)
            user = VerifiedUser.objects.get(username=email)
            print(user)
            if user.is_active:
                return HttpResponseRedirect('/apply/')
            else:
                user.set_hash()
                context = {'error_heading': 'A Verification link has been sent to your email account',
                           'error_message': 'Please click on the link that has been'
                                            ' sent to your email account to verify'
                                            ' your email and continue login again',
                           "resend": True}
        except VerifiedUser.DoesNotExist:
            context = {'error_heading': 'Seems like your are not registered yet',
                       'error_message': 'Please SignUp to continue'}
    return render(request, 'login/login.html', context=context)
