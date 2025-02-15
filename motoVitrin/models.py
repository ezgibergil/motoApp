from django.contrib.auth.models import User 
from django.db import models



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "motoVitrin_category"

    def __str__(self):
        return self.name



class Sale(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    customer_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.customer_name} - {self.amount} ₺"
    
class Siparis(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    urun_adi = models.CharField(max_length=255)
    miktar = models.PositiveIntegerField()
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    durum = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.urun_adi} - {self.kullanici.username}"

