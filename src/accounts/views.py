from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView
from django.core.mail import send_mail
from django.conf import settings

from accounts.forms import AccountCreateForm, AccountPasswordForm, AccountUpdateForm, ContactUs

from .models import User
# Create your views here.


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_redirect_url(self):
        return reverse('testify:index')


class AccountLogoutViev(LogoutView):
    template_name = 'accounts/logout.html'


class AccountPasswordView(PasswordChangeView):
    template_name = 'accounts/password.html'
    form_class = AccountPasswordForm
    success_url = reverse_lazy('accounts:profile')


class AccountCreateView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('testify:index')


class AccountUpdateView(UpdateView):
    template_name = 'accounts/profile.html'
    model = User
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


class ContactUsView(FormView):
    template_name = 'accounts/contact_us.html'
    extra_context = {'title': 'Send us a message!'}
    success_url = reverse_lazy('testify:index')
    form_class = ContactUs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=request.user.email,
                recipient_list=settings.EMAIL_HOST_RECIPIENT.split(':'),
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
