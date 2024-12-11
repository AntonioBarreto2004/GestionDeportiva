from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from ..models import Anthropometric, Athlete


@api_view(['GET'])
def compare_changes(request):
    # Obtiene el parámetro de consulta 'athlete_id'
    athlete_id = request.query_params.get('athlete_id')
    # Obtiene el parámetro de consulta 'athlete_ids'
    athlete_ids = request.query_params.getlist('athlete_ids')

    # Obtiene la fecha actual y la fecha hace tres meses
    today = timezone.now().date()
    three_months_ago = today - timedelta(days=90)

    # Filtra registros antropométricos según los parámetros de consulta y la fecha de control
    if athlete_id:
        anthropometric_records = Anthropometric.objects.filter(
            Q(athlete_id=athlete_id),
            controlDate__range=[three_months_ago, today],
        ).order_by('controlDate')
        # Obtiene el atleta correspondiente al athlete_id
        athletes = [Athlete.objects.get(id=athlete_id)]
    elif athlete_ids:
        anthropometric_records = Anthropometric.objects.filter(
            Q(athlete_id__in=athlete_ids),
            controlDate__range=[three_months_ago, today],
        ).order_by('athlete_id', 'controlDate')
        # Obtiene los atletas correspondientes a los athlete_ids
        athletes = Athlete.objects.filter(id__in=athlete_ids)
    else:
        anthropometric_records = Anthropometric.objects.filter(
            controlDate__range=[three_months_ago, today],
        ).order_by('athlete_id', 'controlDate')
        # Obtiene todos los atletas
        athletes = Athlete.objects.all()

    comparison_data = []
    for athlete in athletes:
        # Crea un diccionario para almacenar los datos de comparación del atleta
        athlete_data = {
            'athlete': f"{athlete.people.name} {athlete.people.last_name}",
            'data': [],
        }
        # Filtra los registros antropométricos del atleta
        records = anthropometric_records.filter(athlete_id=athlete.id)
        for i in range(1, len(records)):
            previous_record = records[i - 1]
            current_record = records[i]
            # Crea un diccionario para almacenar la comparación entre registros
            comparison = {
                'controlDate_previous': previous_record.controlDate,
                'controlDate_current': current_record.controlDate,
            }
            # Compara cada campo antropométrico
            for field in Anthropometric._meta.get_fields():
                field_name = field.name
                # Salta los campos no necesarios
                if field_name in ['id', 'athlete', 'controlDate', 'updated_date']:
                    continue
                previous_value = getattr(previous_record, field_name)
                current_value = getattr(current_record, field_name)
                if previous_value != current_value:
                    comparison[field_name] = {
                        'previous_value': previous_value,
                        'current_value': current_value,
                    }
            # Verifica si hay cambios y agrega la comparación a los datos del atleta
            if len(comparison) > 2:  # Verifica que haya campos comparados además de las fechas
                athlete_data['data'].append(comparison)
        # Verifica si hay datos de comparación y agrega al atleta a los datos de comparación
        if athlete_data['data']:
            comparison_data.append(athlete_data)

    # Prepara la respuesta con los datos de comparación
    if not comparison_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'No hay cambios disponibles para los atletas especificados.',
            'status': False,
            'data': None
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Datos de los registros antropométricos comparados existosamente!',
            'status': True,
            'data': comparison_data
        }

    return Response(data=response_data)









