from django.db import models

# Create your models here.
from django.conf import settings

class ADOperation(models.Model):
    """Log of AD operations performed by users"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    operation = models.CharField(max_length=100)
    target = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.operation} on {self.target} by {self.user}"