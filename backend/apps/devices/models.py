from django.db import models


class Device(models.Model):
    """
    Represents a registered ESP32 device in the system.
    One record per physical board.
    """

    device_id = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="Short identifier sent by the device in every MQTT message.",
    )
    name = models.CharField(
        max_length=128,
        help_text="Human-readable name shown in the dashboard.",
    )
    location = models.CharField(
        max_length=255,
        help_text="Physical location, e.g. 'Server Room A'.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive devices are hidden from the dashboard but retain history.",
    )
    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Updated every time a reading arrives from this device.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return f"{self.name} ({self.device_id})"