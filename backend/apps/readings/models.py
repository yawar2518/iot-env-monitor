from django.db import models


class Reading(models.Model):
    """
    A single telemetry snapshot from one device.
    This table is converted to a TimescaleDB hypertable in migrations.
    Partition column: timestamp.
    """

    device = models.ForeignKey(
        'devices.Device',
        on_delete=models.PROTECT,
        related_name='readings',
        help_text="The device that produced this reading.",
    )
    timestamp = models.DateTimeField(
        db_index=True,
        help_text="Moment the reading was taken. Hypertable partition column.",
    )
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Temperature in degrees Celsius.",
    )
    humidity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Relative humidity as a percentage (0–100).",
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Reading'
        verbose_name_plural = 'Readings'
        # Composite index for the most common query pattern:
        # "give me all readings for device X in time range Y–Z"
        indexes = [
            models.Index(fields=['device', 'timestamp']),
        ]

    def __str__(self):
        return (
            f"{self.device.device_id} | "
            f"{self.timestamp:%Y-%m-%d %H:%M:%S} | "
            f"{self.temperature}°C {self.humidity}%"
        )