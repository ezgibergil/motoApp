from django.db import models
from django.contrib.auth.models import User
class Siparis(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    urun_adi = models.CharField(max_length=255)
    miktar = models.PositiveIntegerField()
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    durum = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.urun_adi} - {self.kullanici.username}"