from django.urls.conf import path

from . import views

app_name = 'testify'

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('test/<str:uuid>', views.TestDetailView.as_view(), name='test'),
    path('<str:uuid>/start', views.TestRunnerView.as_view(), name='start'),
    path('<str:uuid>/next/', views.QuestionView.as_view(), name='question'),
    path('<str:uuid>/restart', views.restart_test, name='restart'),
]

handler404 = views.error_404
handler500 = views.error_500
handler400 = views.error_400
handler403 = views.error_403
