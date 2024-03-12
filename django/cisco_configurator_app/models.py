from django.db import models
from django.db.models import Sum

# Create your models here.


class Router_Model(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Router_Interfaces(models.Model):
    port_name = models.CharField(max_length=100)
    router = models.ForeignKey(Router_Model, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.port_name