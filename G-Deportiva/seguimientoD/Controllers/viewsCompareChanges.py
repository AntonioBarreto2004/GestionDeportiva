from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ..models import *
from datetime import datetime, timedelta

@api_view(['GET'])
def compare_changes(request):
    three_months_ago = datetime.now() - timedelta(days=3 * 30)
    users = Anthropometric.objects.values('athlete_id').distinct()
    changes_detected = []

    for user in users:
        user_records = Anthropometric.objects.filter(
            athlete_id=user['athlete_id'],
            atpt_created_date__lt=three_months_ago
        )

        for record in user_records:
            latest_update = AnthropometricHistory.objects.filter(
                anthropometric__athlete_id=record.athlete_id,
                atpt_controlDate__gte=three_months_ago
            ).order_by('-atpt_controlDate').first()

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

    if changes_detected:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Cambios detectados después de tres meses',
            'status': True,
            'changes_detected': changes_detected,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'No se detectaron cambios después de tres meses',
            'status': False,
        }
        return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

