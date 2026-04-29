from django.urls import path
from .views import AddScheduleView, TodayScheduleView, MarkTakenView

urlpatterns=[
    path('add/', AddScheduleView.as_view(), name='add-schedule'),
    path('today/', TodayScheduleView.as_view(), name='today-schedule'),
    path('mark-taken/<int:pk>/', MarkTakenView.as_view(), name='mark-taken'),
]