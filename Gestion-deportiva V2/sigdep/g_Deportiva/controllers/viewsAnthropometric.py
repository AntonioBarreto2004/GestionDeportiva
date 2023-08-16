from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Q 
from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from ..models import *

@api_view(['GET'])
def list_anthro(request):
    athlete_id = request.GET.get('athlete_id')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    gender = request.GET.get('gender')
    arm = request.GET.get('arm')
    chest = request.GET.get('chest')
    hip = request.GET.get('hip')
    twin = request.GET.get('twin')
    humerus = request.GET.get('humerus')
    femur = request.GET.get('femur')
    wrist = request.GET.get('wrist')
    triceps = request.GET.get('triceps')
    supraspinal = request.GET.get('supraspinal')
    pectoral = request.GET.get('pectoral')
    zise = request.GET.get('zise')
    weight = request.GET.get('weight')
    bmi = request.GET.get('bmi')

    query = Q()

    if athlete_id:
        query &= Q(athlete_id=athlete_id)

    filters = {}

    if min_age and max_age:
        max_birthdate = datetime.now().date() - relativedelta(years=int(min_age))
        min_birthdate = datetime.now().date() - relativedelta(years=int(max_age))
        query &= Q(athlete__people__birthdate__range=(min_birthdate, max_birthdate))

    if gender:
        query &= Q(athlete__people__gender=gender)

    if arm:
        filters['arm'] = int(arm)
    if chest:
        filters['chest'] = chest
    if hip:
        filters['hip'] = int(hip)
    if twin:
        filters['twin'] = int(twin)
    if humerus:
        filters['humerus'] = int(humerus)
    if femur:
        filters['femur'] = int(femur)
    if wrist:
        filters['wrist'] = int(wrist)
    if triceps:
        filters['triceps'] = int(triceps)
    if supraspinal:
        filters['supraspinal'] = int(supraspinal)
    if pectoral:
        filters['pectoral'] = int(pectoral)
    if zise:
        filters['zise'] = int(zise)
    if weight:
        filters['weight'] = int(weight)
    if bmi:
        filters['bmi'] = int(bmi)

    if filters:
        query &= Q(**filters)

    queryset = Anthropometric.objects.filter(query)
    serialized_data = []

    for item in queryset:
        birthdate = item.athlete.people.birthdate
        age = relativedelta(datetime.now().date(), birthdate).years

        data = {
            'id': item.id,
            'athlete_id': item.athlete.id,
            'athlete_name': f"{item.athlete.people.name} {item.athlete.people.last_name}",
            'gender': item.athlete.people.gender,
            'birthdate': birthdate,
            'age': age,
            'controlDate': item.controlDate,
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
        }
        serialized_data.append(data)

    if serialized_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos encontrados exitosamente',
            'data': serialized_data
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No se encontraron datos',
            'data': []
        }

    return Response(response_data)

    
@api_view(['POST'])
def create_anthro(request):
    serializer_create = AnthropometricSerializer(data=request.data)
    serializer_create.is_valid(raise_exception=True)

    athlete_id = serializer_create.validated_data['athlete']

    # Calcula la fecha actual
    current_date = datetime.now().date()

    # Calcula la fecha hace 90 días
    min_date = current_date - timedelta(days=90)

    # Verifica si ya existe un registro para el atleta en la misma fecha
    existing_record = Anthropometric.objects.filter(athlete_id=athlete_id, controlDate=current_date).exists()

    if existing_record:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Ya se ha registrado un antropométrico para este atleta hoy',
            'status': True,
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
            'status': True,
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
            'status': True,
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
            'status': True,
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


@api_view(['GET'])
def list_anthro_filters(request):
    athlete_id = request.GET.get('athlete_id')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    gender = request.GET.get('gender')
    arm = request.GET.get('arm')
    chest = request.GET.get('chest')
    hip = request.GET.get('hip')
    twin = request.GET.get('twin')
    humerus = request.GET.get('humerus')
    femur = request.GET.get('femur')
    wrist = request.GET.get('wrist')
    triceps = request.GET.get('triceps')
    supraspinal = request.GET.get('supraspinal')
    pectoral = request.GET.get('pectoral')
    zise = request.GET.get('zise')
    weight = request.GET.get('weight')
    bmi = request.GET.get('bmi')

    query = Q()

    if athlete_id:
        query &= Q(athlete_id=athlete_id)

    filters = {}

    if min_age and max_age:
        max_birthdate = datetime.now().date() - relativedelta(years=int(min_age))
        min_birthdate = datetime.now().date() - relativedelta(years=int(max_age))
        query &= Q(athlete__people__birthdate__range=(min_birthdate, max_birthdate))

    if gender:
        query &= Q(athlete__people__gender=gender)

    if arm:
        filters['arm'] = int(arm)
    if chest:
        filters['chest'] = chest
    if hip:
        filters['hip'] = int(hip)
    if twin:
        filters['twin'] = int(twin)
    if humerus:
        filters['humerus'] = int(humerus)
    if femur:
        filters['femur'] = int(femur)
    if wrist:
        filters['wrist'] = int(wrist)
    if triceps:
        filters['triceps'] = int(triceps)
    if supraspinal:
        filters['supraspinal'] = int(supraspinal)
    if pectoral:
        filters['pectoral'] = int(pectoral)
    if zise:
        filters['zise'] = int(zise)
    if weight:
        filters['weight'] = int(weight)
    if bmi:
        filters['bmi'] = int(bmi)

    if filters:
        query &= Q(**filters)

    queryset = Anthropometric.objects.filter(query)
    serialized_data = []

    for item in queryset:
        birthdate = item.athlete.people.birthdate
        age = relativedelta(datetime.now().date(), birthdate).years

        data = {
            'id': item.id,
            'athlete_id': item.athlete.id,
            'athlete_name': f"{item.athlete.people.name} {item.athlete.people.last_name}",
            'gender': item.athlete.people.gender,
            'birthdate': birthdate,
            'age': age,
            'controlDate': item.controlDate,
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
        }
        serialized_data.append(data)

    if serialized_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos encontrados exitosamente',
            'data': serialized_data
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No se encontraron datos',
            'data': []
        }

    return Response(response_data)