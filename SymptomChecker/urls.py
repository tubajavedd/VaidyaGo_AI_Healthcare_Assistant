from django.urls import path
from .views import PatientSummaryView, UpdateInputSummaryView, ConditionDetailView, SaveReportView, SymptomAuditLogView, ConfirmMedicationDoseView

urlpatterns = [
    path('patients/<str:patient_id>/', PatientSummaryView.as_view()),
    path('patients/<str:patient_id>/input-summary/', UpdateInputSummaryView.as_view()),
    path('patients/<str:patient_id>/condition/<str:condition_name>/', ConditionDetailView.as_view()),
    path('patients/<str:patient_id>/save-report/', SaveReportView.as_view()),
    path('patients/<str:patient_id>/audit-log/', SymptomAuditLogView.as_view()),
    path('patients/<str:patient_id>/confirm-dose/', ConfirmMedicationDoseView.as_view()),
]






















# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import SymptomLogViewSet

# router = DefaultRouter()
# router.register(r'logs', SymptomLogViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]
