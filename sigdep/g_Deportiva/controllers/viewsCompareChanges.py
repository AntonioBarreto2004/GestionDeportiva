# from datetime import timedelta
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.db.models import Q
# from django.utils import timezone
# from ..models import Anthropometric


# @api_view(['GET'])
# def compare_changes(request):
#     athlete_id = request.query_params.get('athlete_id')

#     today = timezone.now().date()
#     one_day_ago = today - timedelta(days=1)


#     # Obtener los IDs de atletas de la consulta de parámetros
#     athlete_ids = request.query_params.getlist('athlete_ids')

#     # Filtrar registros de Anthropometric para el atleta específico o para los IDs de atletas especificados con fecha de control dentro de los últimos 3 meses
#     anthropometric_records = Anthropometric.objects.filter(
#         Q(athlete_id=athlete_id) | Q(athlete_id__in=athlete_ids),
#         controlDate__range=[one_day_ago, today],
#     ).order_by('controlDate')

#     # Comparar los cambios y registrarlos en una lista
#     changes = []
#     for i in range(1, len(anthropometric_records)):
#         previous_record = anthropometric_records[i - 1]
#         current_record = anthropometric_records[i]

#         changes.append({
#             'controlDate': current_record.controlDate,
#             'changes': {
#                 'arm': {
#                     'previous_value': previous_record.arm,
#                     'current_value': current_record.arm,
#                 },
#                 'chest': {
#                     'previous_value': previous_record.chest,
#                     'current_value': current_record.chest,
#                 },
#                 'hip': {
#                     'previous_value': previous_record.hip,
#                     'current_value': current_record.hip,
#                 },
#                 'twin': {
#                     'previous_value': previous_record.twin,
#                     'current_value': current_record.twin,
#                 },
#                 # Agregar los demás campos antropométricos aquí
#             },
#         })

#     response_data = {
#         'code': status.HTTP_200_OK,
#         'message': 'Datos de los registros antropométricos comparados existosamente!',
#         'status': True,
#         'data': changes
#     }

#     if not changes:
#         response_data = {
#             'code': status.HTTP_200_OK,
#             'message': 'No hay cambios disponibles para los atletas especificados.',
#             'status': False,
#             'data': None
#         }

#     return Response(data=response_data)