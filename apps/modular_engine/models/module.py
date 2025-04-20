from django.db import models

class Module(models.Model):
    STATUS_CHOICES = (
        ('installed', 'Installed'),
        ('uninstalled', 'Uninstalled'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uninstalled')
    installed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=20, default="1.0")


    def __str__(self):
        return self.name
