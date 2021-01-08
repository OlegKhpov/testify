from django.urls.conf import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.AccountLoginView.as_view(), name='login'),
    path('logout', views.AccountLogoutViev.as_view(), name='logout'),
    path('register', views.AccountCreateView.as_view(), name='register'),
    path('profile', views.AccountUpdateView.as_view(), name='profile'),
    path('password/', views.AccountPasswordView.as_view(), name='password'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us')
]
