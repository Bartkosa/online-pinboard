from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),

    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('habit-create/', HabitCreate.as_view(), name='habit-create'),
    path('event-create/', EventCreate.as_view(), name='event-create'),

    path('task-edit/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('habit-edit/<int:pk>', HabitUpdate.as_view(), name='habit-update'),
    path('event-edit/<int:pk>', EventUpdate.as_view(), name='event-update'),

    path('task-delete/<int:pk>', DeleteTask.as_view(), name='task-delete'),
    path('habit-delete/<int:pk>', DeleteHabit.as_view(), name='habit-delete'),
    path('event-delete/<int:pk>', DeleteEvent.as_view(), name='event-delete'),

    path('calendar/<int:year>/<str:month>/', calendar_view, name='calendar'),
]