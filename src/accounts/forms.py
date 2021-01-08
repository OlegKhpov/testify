from django import forms
from django.forms import ModelForm, Form, fields
from accounts.models import User
from django.contrib.auth.forms import PasswordChangeForm


class AccountCreateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'location',
            'birth_date',
            'show_result_popup',
            'profile_img',
        ]


class AccountUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'location',
            'birth_date',
            'show_result_popup',
            'profile_img',
        ]


class AccountPasswordForm(PasswordChangeForm):
    pass


class ContactUs(Form):
    subject = fields.CharField(max_length=256, empty_value='Message from Testify')
    message = fields.CharField(widget=forms.Textarea)
