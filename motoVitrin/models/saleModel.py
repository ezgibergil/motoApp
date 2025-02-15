from django.contrib.auth.models import User 
from django.db import models
from motoVitrin.models import Category



class Sale(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    customer_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.customer_name} - {self.amount} ₺"