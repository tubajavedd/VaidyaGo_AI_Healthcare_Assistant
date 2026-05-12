from django.urls import path
from .views import (
    DiagnosticAnalyzeView, 
    DiagnosticHistoryView, 
    DiagnosticDetailView, 
    DiagnosticByBodyPartView
)

urlpatterns = [
    path('analyze/', DiagnosticAnalyzeView.as_view(), name='diagnostic-analyze'),
    path('history/', DiagnosticHistoryView.as_view(), name='diagnostic-history'),
    path('<int:pk>/', DiagnosticDetailView.as_view(), name='diagnostic-detail'),
    path('body-part/<str:body_part>/', DiagnosticByBodyPartView.as_view(), name='diagnostic-body-part'),
]
