from django.urls import path
from .views import AdminProfileView, DisconnectGoogle
from .views import pending_doctors, approve_doctor, reject_doctor

urlpatterns = [
    path('profile/', AdminProfileView.as_view()),
    path('profile/edit/', AdminProfileView.as_view()), 
    path('profile/disconnect-google/', DisconnectGoogle.as_view()),

    path('doctors/pending/', pending_doctors),
    path('doctors/approve/<int:doctor_id>/', approve_doctor),
    path('doctors/reject/<int:doctor_id>/', reject_doctor),
  
]
