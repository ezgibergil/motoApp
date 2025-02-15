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
