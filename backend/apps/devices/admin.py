from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'location', 'is_active', 'last_seen', 'created_at']
    list_filter = ['is_active', 'location']
    search_fields = ['device_id', 'name', 'location']
    readonly_fields = ['created_at', 'last_seen']
    ordering = ['name']