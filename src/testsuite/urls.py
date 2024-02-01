from django.urls import path

from . import views
from .views import slow_func

app_name = 'testsuite'

urlpatterns = [
    path('', views.TestListView.as_view(), name='list'),

    path('<int:pk>/start/', views.StartTestView.as_view(), name='start'),

    # path('<int:pk>/question/<int:seq_nr>', views.TestRunView.as_view(), name='testrun_step'),
    path('<int:pk>/next/', views.TestRunView.as_view(), name='next'),

    path('leader/', views.UserLeaderBoardListView.as_view(), name='leader_board'),

    path('slow', slow_func, name='slow'),

]
