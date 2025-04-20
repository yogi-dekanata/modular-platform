from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    barcode = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        """Soft Delete Override"""
        self.is_deleted = True
        self.save()
