from django.urls import path
from .views import (
    AccountSettingsView,
    ChangePasswordView,
    Toggle2FAView,
    LoginHistoryView,
    DeactivateAccountView,
    RequestDataDeletionView,
    SwitchLanguageView,
)

urlpatterns = [
    path("account-settings/", AccountSettingsView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("toggle-2fa/", Toggle2FAView.as_view()),
    path("login-history/", LoginHistoryView.as_view()),
    path("deactivate-account/", DeactivateAccountView.as_view()),
    path("request-data-deletion/", RequestDataDeletionView.as_view()),
    path("switch-language/", SwitchLanguageView.as_view()),
]
