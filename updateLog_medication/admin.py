from django.contrib import admin
from .models import AccountSettings, UpdateLog

admin.site.register(AccountSettings)
admin.site.register(UpdateLog)
