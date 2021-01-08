from django.urls import path
from testify.api.views import TestListCreateView, TestUpdateDeleteView

app_name = 'api_testify'

urlpatterns = [
    path('tests', TestListCreateView.as_view(), name='tests'),
    path('tests/<int:pk>', TestUpdateDeleteView.as_view(), name='tests_update')
]
