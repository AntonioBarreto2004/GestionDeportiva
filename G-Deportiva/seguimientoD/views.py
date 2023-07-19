from django.db.models.signals import pre_save
from django.dispatch import receiver
import pytz
from datetime import datetime
from .models import *
from .serializer import *

#Actualizar fecha de cambios
@receiver(pre_save, sender=Anthropometric)
def profile_pre_save(sender, instance, **kwargs):
    if instance.pk:
        original_instance = Anthropometric.objects.get(pk=instance.pk)
        if (
            original_instance.atpt_arm != instance.atpt_arm
            or original_instance.atpt_chest != instance.atpt_chest
            or original_instance.atpt_hip != instance.atpt_hip
            or original_instance.atpt_calf != instance.atpt_calf
            or original_instance.atpt_humerus != instance.atpt_humerus
            or original_instance.atpt_femur != instance.atpt_femur
            or original_instance.atpt_wrist != instance.atpt_wrist
            or original_instance.atpt_triceps != instance.atpt_triceps
            or original_instance.atpt_suprailiac != instance.atpt_suprailiac
            or original_instance.atpt_pectoral != instance.atpt_pectoral
            or original_instance.atpt_height != instance.atpt_height
            or original_instance.atpt_weight != instance.atpt_weight
            or original_instance.atpt_bmi != instance.atpt_bmi
        ):
            colombia_timezone = pytz.timezone('America/Bogota')
            # Obtener la fecha y hora actual en la zona horaria de Colombia
            current_time = datetime.now(colombia_timezone)
            # Asignar la fecha y hora actual en la zona horaria de Colombia al campo atpt_updated_date
            instance.atpt_updated_date = current_time
