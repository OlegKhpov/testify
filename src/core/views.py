from django.shortcuts import render # noqa

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredBaseMixin(LoginRequiredMixin):
    login_url = 'accounts/login.html'
