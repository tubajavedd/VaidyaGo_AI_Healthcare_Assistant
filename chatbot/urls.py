from django.urls import path
from .views import (
    chat_view, 
    available_tools_view, 
    tools_description_view,
    upload_prescription_api,
    prescription_details_api,
    prescription_medicines_api,
    list_prescriptions_api,
    all_apis_info_view
)

urlpatterns = [
    path("chat/", chat_view, name="chat"),
    path("tools/", available_tools_view, name="available_tools"),
    path("tools-description/", tools_description_view, name="tools_description"),
    path("all-apis/", all_apis_info_view, name="all_apis_info"),
    
    # Prescription Management APIs
    path("upload-prescription/", upload_prescription_api, name="upload_prescription"),
    path("prescriptions/list/", list_prescriptions_api, name="list_prescriptions"),
    path("prescriptions/<int:prescription_id>/details/", prescription_details_api, name="prescription_details"),
    path("prescriptions/<int:prescription_id>/medicines/", prescription_medicines_api, name="prescription_medicines"),
]

