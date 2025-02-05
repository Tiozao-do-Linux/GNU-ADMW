from django.db import models
from django.conf import settings

class ADUser(models.Model):
    """Model to represent Active Directory users"""
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'AD User'
        verbose_name_plural = 'AD Users'

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

class ADGroup(models.Model):
    """Model to represent Active Directory groups"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(ADUser, related_name='groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'AD Group'
        verbose_name_plural = 'AD Groups'

    def __str__(self):
        return self.name

class AuditLog(models.Model):
    """Model to track changes made to AD objects"""
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('MODIFY', 'Modify'),
        ('DELETE', 'Delete'),
        ('ENABLE', 'Enable'),
        ('DISABLE', 'Disable'),
        ('PASSWORD', 'Password Reset'),
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    target_type = models.CharField(max_length=50)  # 'user' or 'group'
    target_name = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} {self.target_type}: {self.target_name} by {self.actor}"

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
