from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from ..models import *

#METODO GET (LISTAR)
@api_view(['GET'])
def list_anthro(request):
    athlete_id = request.GET.get('athlete_id')
    control_date = request.GET.get('control_date')
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

    queryset = Anthropometric.objects.all()

    if athlete_id:
        queryset = queryset.filter(athlete_id=athlete_id)
    if control_date:
        queryset = queryset.filter(controlDate=control_date)
    if arm:
        queryset = queryset.filter(arm=arm)
    if chest:
        queryset = queryset.filter(chest=chest)
    if hip:
        queryset = queryset.filter(hip=hip)
    if twin:
        queryset = queryset.filter(twin=twin)
    if humerus:
        queryset = queryset.filter(humerus=humerus)
    if femur:
        queryset = queryset.filter(femur=femur)
    if wrist:
        queryset = queryset.filter(wrist=wrist)
    if triceps:
        queryset = queryset.filter(triceps=triceps)
    if supraspinal:
        queryset = queryset.filter(supraspinal=supraspinal)
    if pectoral:
        queryset = queryset.filter(pectoral=pectoral)
    if zise:
        queryset = queryset.filter(zise=zise)
    if weight:
        queryset = queryset.filter(weight=weight)
    if bmi:
        queryset = queryset.filter(bmi=bmi)


    if not queryset.exists():
        return Response(
            data={'code': status.HTTP_200_OK, 
            'message': 'No se encontraron datos existentes', 
            'status': False,
            'data': None
            })
    
    
    data = []
    for item in queryset:
        serializer = AnthropometricSerializer(item)
        person_id = serializer.data['athlete']  # Remover el ID de la persona del objeto
        atleta = Athlete.objects.get(id=person_id)
        item_data = serializer.data
        item_data['athlete'] = f"{atleta.people.name} {atleta.people.last_name}"  # Añadir el nombre de la persona
        data.append(item_data)

    responde_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Datos encontrados exitosamente',
            'data': data
        }

    return Response (responde_data)
    
@api_view(['POST'])
def create_anthro(request):
    serializer_create = AnthropometricSerializer(data=request.data)
    serializer_create.is_valid(raise_exception=True)

    # Validaciones para campos individuales
    if serializer_create.validated_data['arm'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "arm" no puede ser negativo',
            'status': False,
            'data': None
        })

    if not 0 < len(serializer_create.validated_data['chest']) <= 45:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El campo "chest" debe tener entre 1 y 45 caracteres',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['hip'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "hip" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['twin'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "twin" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['humerus'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "humerus" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['femur'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "femur" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['wrist'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "wrist" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['triceps'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "triceps" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['supraspinal'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "supraspinal" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['pectoral'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "pectoral" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['zise'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "zise" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['weight'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "weight" no puede ser negativo',
            'status': False,
            'data': None
        })

    if serializer_create.validated_data['bmi'] < 0:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'El valor del campo "bmi" no puede ser negativo',
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