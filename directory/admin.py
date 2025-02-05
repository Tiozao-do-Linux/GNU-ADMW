from django.contrib import admin

# Register your models here.
from .models import ADUser, ADGroup, AuditLog, ADOperation

admin.site.register(ADUser)
admin.site.register(ADGroup)
admin.site.register(AuditLog)
admin.site.register(ADOperation)

