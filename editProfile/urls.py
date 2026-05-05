from django.urls import path
from .views import EditProfileView

urlpatterns = [
    path("edit-profile/", EditProfileView.as_view()),
]
