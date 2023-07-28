import requests
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ..models import Anthropometric, Athlete
from datetime import datetime, timedelta

@api_view(['GET'])
def compare_changes(request):
    try:
        three_months_ago = datetime.now() - timedelta(days=3 * 30)
        users = Anthropometric.objects.values('athlete_id').distinct()
        changes_detected = []

        for user in users:
            user_records = Anthropometric.objects.filter(
                athlete_id=user['athlete_id'],
                atpt_created_date__lt=three_months_ago
            )

            for record in user_records:
                latest_update = Anthropometric.objects.filter(
                    athlete_id=record.athlete_id,
                    atpt_created_date__gte=three_months_ago
                ).order_by('-atpt_created_date').first()

                if latest_update:
                    relevant_fields = [
                        'atpt_arm', 'atpt_chest', 'atpt_hip', 'atpt_calf', 'atpt_humerus',
                        'atpt_femur', 'atpt_wrist', 'atpt_triceps', 'atpt_suprailiac',
                        'atpt_pectoral', 'atpt_height', 'atpt_weight', 'atpt_bmi'
                    ]

                    changes_detected_fields = []

                    for field in relevant_fields:
                        initial_value = getattr(record, field)
                        latest_value = getattr(latest_update, field)

                        if initial_value != latest_value:
                            changes_detected_fields.append({
                                'field': field,
                                'initial_value': initial_value,
                                'latest_value': latest_value
                            })

                    if changes_detected_fields:
                        athlete = Athlete.objects.get(id=record.athlete_id)
                        athlete_name = athlete.at_user.first().get_full_name() if athlete.at_user.exists() else ''
                        changes_detected.append({
                            'user_id': record.athlete_id.id,
                            'athlete_name': athlete_name,
                            'record_id': record.pk,
                            'changes': changes_detected_fields
                        })

                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Cambios detectados después de tres meses',
                    'status': True,
                    'changes_detected': changes_detected,
                    'data': None

                }

        if changes_detected:
            return Response(response_data)
        else:
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': 'No se detectaron cambios después de tres meses',
                'status': False,
                'data': None
            }
            return Response(responde_data)
        
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)
