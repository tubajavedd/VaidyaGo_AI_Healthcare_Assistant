from django.urls import path
from .views import AdminProfileView, DisconnectGoogle

urlpatterns = [
    path('profile/', AdminProfileView.as_view()),
      path('profile/edit/', AdminProfileView.as_view()), 
    path('profile/disconnect-google/', DisconnectGoogle.as_view()),
  
]
