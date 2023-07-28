import requests
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializer import *
from ..models import *

#METODO GET (LISTAR)
@api_view(['GET'])
def list_anthro(request):
    try:
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

        queryset = Anthropometric.objects.all()

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
                data = { 
                    'code': status.HTTP_200_OK, 
                    'message': 'No se encontraron datos existentes', 
                    'status': False,
                    'data': None,
                }
            )
        
        serializer = AnthropometricSerializer(queryset, many=True)
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Datos listados Correctamente',
            'status': True,
            'data': serializer
        }
        return Response(response_data)
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


    #METODO POST (AGREGAR)
@api_view(['POST'])
def create_anthro(request):
        try:
            serializer_create = AnthropometricSerializer(data=request.data)
            serializer_create.is_valid(raise_exception=True)
            validate_data = serializer_create.validated_data
            serializer_create.save()

            if Anthropometric.objects.filter(athlete_id=validate_data['athlete_id']):
                return Response(
                    data={'code': status.HTTP_200_OK, 
                        'message': 'Ya existe un atleta registrado', 
                        'status': False ,
                        'data':None
                        },
                        
                )
            responde_data = {
                'code': status.HTTP_201_CREATED, 
                'message': 'Datos Registrados exitosamente!', 
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
    

    #METODO PATCH (ACTUALIZAR)
@api_view(['PATCH'])
def update_anthro(request, pk):
    try:
        try:
            anthrop = Anthropometric.objects.get(pk=pk)
        except Anthropometric.DoesNotExist:
            return Response(data={'code': '404_NOT_FOUND', 
                                'message': 'Antropometría no encontrada.', 
                                'status': False,
                                'data': None
                                }, 
                            )
        
        serializer = AnthropometricSerializer(anthrop, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_data ={
            'code': status.HTTP_200_OK,
            'message': 'Antropometría actualizada exitosamente',
            'status': True,
            'data': None
        }
        
        return Response(response_data)
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

    #METODO DELETE (ELIMINAR)
@api_view(['DELETE'])
def delete_anthro(request, pk):
    try:
        try:
            anthrop = Anthropometric.objects.get(pk=pk)
        except Anthropometric.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Datos no encontrada.', 
                                'status': False,
                                'data': None
                                }, 
                            )
        
        athlete_name = anthrop.athlete_id.at_user.name
        anthrop.delete()
        
        response_data ={
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Datos de {athlete_name} eliminados exitosamente',
            'status': True,
            'data': None
        }
        
        return Response(response_data)
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


