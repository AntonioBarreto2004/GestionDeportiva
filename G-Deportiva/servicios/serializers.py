from rest_framework import serializers
from .models import *

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ReciboPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReciboPago
        fields = '__all__'
