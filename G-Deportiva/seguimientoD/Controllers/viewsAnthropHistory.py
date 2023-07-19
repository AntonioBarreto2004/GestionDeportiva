from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *
from .viewsCompareChanges import compare_changes

#METODO GET (LISTAR)
@api_view(['GET'])
def list_anthro(request):
    athlete_id = request.GET.get('athlete_id')
    control_date = request.GET.get('control_date')
    arm = request.GET.get('arm')
    chest = request.GET.get('chest')
    hip = request.GET.get('hip')
    calf = request.GET.get('calf')
    humerus = request.GET.get('humerus')
    femur = request.GET.get('femur')
    wrist = request.GET.get('wrist')
    triceps = request.GET.get('triceps')
    suprailiac = request.GET.get('suprailiac')
    pectoral = request.GET.get('pectoral')
    height = request.GET.get('height')
    weight = request.GET.get('weight')
    bmi = request.GET.get('bmi')

    queryset = AnthropometricHistory.objects.all()

    if athlete_id:
        queryset = queryset.filter(athlete_id=athlete_id)
    if control_date:
        queryset = queryset.filter(atpt_controlDate=control_date)
    if arm:
        queryset = queryset.filter(atpt_arm=arm)
    if chest:
        queryset = queryset.filter(atpt_chest=chest)
    if hip:
        queryset = queryset.filter(atpt_hip=hip)
    if calf:
        queryset = queryset.filter(atpt_calf=calf)
    if humerus:
        queryset = queryset.filter(atpt_humerus=humerus)
    if femur:
        queryset = queryset.filter(atpt_femur=femur)
    if wrist:
        queryset = queryset.filter(atpt_wrist=wrist)
    if triceps:
        queryset = queryset.filter(atpt_triceps=triceps)
    if suprailiac:
        queryset = queryset.filter(atpt_suprailiac=suprailiac)
    if pectoral:
        queryset = queryset.filter(atpt_pectoral=pectoral)
    if height:
        queryset = queryset.filter(atpt_height=height)
    if weight:
        queryset = queryset.filter(atpt_weight=weight)
    if bmi:
        queryset = queryset.filter(atpt_bmi=bmi)


    if not queryset.exists():
        return Response(
            data={'code': '404_NOT_FOUND', 
            'message': 'No se encontraron datos existentes', 
            'status': False},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AnthropometricSerializer(queryset, many=True)
    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Datos listados Correctamente',
        'status': True
    }
    return Response(data=(response_data, serializer.data))
    


    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_anthro(request):
    serializer_create = AnthropoHistorySerializer(data=request.data)
    serializer_create.is_valid(raise_exception=True)
    validated_data = serializer_create.validated_data

    athlete_id = validated_data['athlete_id']
    control_date = validated_data['atpt_controlDate']

    if AnthropometricHistory.objects.filter(athlete_id=athlete_id, atpt_controlDate=control_date).exists():
        return Response(
            data={'code': status.HTTP_409_CONFLICT, 'message': 'Ya existe un registro para esta fecha', 'status': False},
            status=status.HTTP_409_CONFLICT
        )

    serializer_create.save()

    response_data = {
        'code': status.HTTP_201_CREATED,
        'message': 'Datos registrados exitosamente!',
        'status': True
    }
    return Response(data=response_data, status=status.HTTP_201_CREATED)



changes_detected = []  # Variable para almacenar los cambios detectados
    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_anthro(request, pk):
    try:
        anthrop = AnthropometricHistory.objects.get(pk=pk)
    except AnthropometricHistory.DoesNotExist:
        return Response(data={'code': '404_NOT_FOUND', 
                              'message': 'Antropometría no encontrada.', 
                              'status': False}, 
                              status=status.HTTP_404_NOT_FOUND
                        )
    
    serializer = AnthropoHistorySerializer(anthrop, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    response_data ={
        'code': status.HTTP_200_OK,
        'message': 'Datos actualizados exitosamente',
        'status': True
    }
    
    return Response(data=response_data, status=status.HTTP_200_OK)

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_anthro(request, pk):
    try:
        anthrop = AnthropometricHistory.objects.get(pk=pk)
    except AnthropometricHistory.DoesNotExist:
        return Response(data={'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 
                              'message': 'Datos no encontrada.', 
                              'status': False}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
    
    athlete_name = anthrop.athlete_id.at_user.name
    anthrop.delete()
    
    response_data ={
        'code': status.HTTP_204_NO_CONTENT,
        'message': f'Datos de {athlete_name} eliminados exitosamente',
        'status': True
    }
    
    return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_changes(request):
    # Lógica para obtener los cambios llamando a la función compare_changes en el archivo comparator.py
    changes_detected = compare_changes()

    return Response(changes_detected)


