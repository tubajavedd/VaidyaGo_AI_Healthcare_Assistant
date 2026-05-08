from django.urls import path
from .views import UploadDocumentAPIView

urlpatterns = [
    path("upload-document/", UploadDocumentAPIView.as_view()),
]