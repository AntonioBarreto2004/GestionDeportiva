from rest_framework import status
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from ..models import *

@api_view(['GET'])
def list_anthro(request):
    athlete_id = request.GET.get('athlete')

    queryset = Anthropometric.objects.all()

    if athlete_id:
        queryset = queryset.filter(athlete_id=athlete_id)

    if not queryset.exists():
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'No se encontraron datos existentes',
            'status': False,
            'data': []
        })

    athlete_data = {}  # Diccionario para agrupar datos por atleta
    for item in queryset:
        serializer = AnthropometricSerializer(item)
        athlete = Athlete.objects.get(id=item.athlete_id)
        item_data = {
            'id': item.id,
            'controlDate': item.controlDate.strftime('%Y-%m-%d'),
            'arm': item.arm,
            'chest': item.chest,
            'hip': item.hip,
            'twin': item.twin,
            'humerus': item.humerus,
            'femur': item.femur,
            'wrist': item.wrist,
            'triceps': item.triceps,
            'supraspinal': item.supraspinal,
            'pectoral': item.pectoral,
            'zise': item.zise,
            'weight': item.weight,
            'bmi': item.bmi,
            'updated_date': item.updated_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }
        
        athlete_name = f"{athlete.people.name} {athlete.people.last_name}"
        if athlete_name in athlete_data:
            athlete_data[athlete_name].append(item_data)
        else:
            athlete_data[athlete_name] = [item_data]

    data = []
    for athlete_name, records in athlete_data.items():
        athlete_entry = {
            'athlete': athlete_name,
            'data': records
        }
        data.append(athlete_entry)

    response_data = {
        'code': status.HTTP_200_OK,
        'status': False,
        'message': 'Datos encontrados exitosamente',
        'data': data
    }

    return Response(response_data)


    
@api_view(['POST'])
def create_anthro(request):
    serializer_create = AnthropometricSerializer(data=request.data)
    serializer_create.is_valid(raise_exception=True)

    athlete_id = serializer_create.validated_data['athlete']

    # Calcula la fecha actual
    current_date = datetime.now().date()

    # Verifica si ya existe un registro para el atleta en la misma fecha
    existing_record = Anthropometric.objects.filter(athlete_id=athlete_id, controlDate=current_date).exists()

    if existing_record:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Ya se ha registrado un antropométrico para este atleta hoy',
            'status': False,
            'data': None
        })

    negative_fields = ['arm', 'hip', 'twin', 'humerus', 'femur', 'wrist', 'triceps', 'supraspinal', 'pectoral', 'zise', 'weight', 'bmi']

    for field_name in negative_fields:
        field_value = serializer_create.validated_data.get(field_name)
        if field_value is not None and field_value < 0:
            return Response({
                'code': status.HTTP_200_OK,
                'message': f'El valor del campo "{field_name}" no puede ser negativo',
                'status': False,
                'data': None
            })

    chest_value = serializer_create.validated_data.get('chest')
    if not 0 < len(chest_value) <= 45:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El campo "chest" debe tener entre 1 y 45 caracteres',
            'status': False,
            'data': None
        })

    serializer_create.save()

    response_data = {
        'code': status.HTTP_201_CREATED,
        'message': 'Datos registrados exitosamente!',
        'status': True,
        'data': None
    }
    return Response(response_data)

@api_view(['PATCH'])
def update_anthro(request, pk):
    try:
        anthrop = Anthropometric.objects.get(pk=pk)
    except Anthropometric.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK, 
            'message': 'Antropometría no encontrada.', 
            'status': False,
            'data': None
        })
    
    serializer = AnthropometricSerializer(anthrop, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    response_data ={
        'code': status.HTTP_200_OK,
        'message': 'Antropometría actualizada exitosamente',
        'status': True,
        'data': None
    }
    
    return Response(data=response_data)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_anthro(request, pk):
    try:
        anthrop = Anthropometric.objects.get(pk=pk)
    except Anthropometric.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK, 
            'message': 'Datos no encontrada.', 
            'status': False,
            'data': None
        })
    
    athlete_name = anthrop.athlete.people.name
    anthrop.delete()
    
    response_data ={
        'code': status.HTTP_200_OK,
        'message': f'Datos de {athlete_name} eliminados exitosamente',
        'status': True,
        'data': None
    }
    
    return Response(data=response_data)