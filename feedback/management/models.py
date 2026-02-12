from django.conf import settings
from django.db import models

class Complaint(models.Model):
    STATUS_OPEN = "open"
    STATUS_PROGRESS = "in_progress"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints")
    title = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_edit(self):
        return self.status != self.STATUS_RESOLVED

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
