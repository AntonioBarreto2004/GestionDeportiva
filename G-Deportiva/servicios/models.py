from django.conf import settings
from django.db import models

# Create your models here.
class Servicio(models.Model):
    nombreServicio = models.CharField(max_length=100)
    descripcionServicio = models.TextField()
    valorServicio = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class ReciboPago(models.Model):
    fechaPago = models.DateField()
    valorPago = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)