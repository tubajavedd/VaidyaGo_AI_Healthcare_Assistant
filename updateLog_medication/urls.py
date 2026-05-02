from django.urls import path
from .views import(
    createUpdateLogView,
    UpdateLogHistoryView
)

urlpatterns = [
    path('create/',createUpdateLogView.as_view(),name="create-update-log"),
    path('history/',UpdateLogHistoryView.as_view(),name="upadate-log-history"),
]