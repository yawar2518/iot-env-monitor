from django.contrib import admin
from .models import Reading


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'temperature', 'humidity']
    list_filter = ['device']
    search_fields = ['device__device_id', 'device__name']
    readonly_fields = ['device', 'timestamp', 'temperature', 'humidity']
    ordering = ['-timestamp']