from datetime import datetime
import re
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Sports
from ..serializers import SportsSerializer

@api_view(['GET'])
def list_sports(request):
    try:
        id = request.GET.get('id')
        sport_name = request.GET.get('sport_name')
        creation_date = request.GET.get('creation_date')

        queryset = Sports.objects.all()

        if id:
            queryset = queryset.filter(id=id)
        if sport_name:
            queryset = queryset.filter(sport_name=sport_name)
        if creation_date:
            queryset = queryset.filter(creation_date=creation_date)

        if not queryset.exists():
            return Response(
                data = { 
                    'code': status.HTTP_200_OK, 
                    'message': 'No se encontraron datos existentes', 
                    'status': False,
                    'data': None,
                }
            )

        serializer = SportsSerializer(queryset, many=True)
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos Encontrados',
            'data': serializer.data
        }
        return Response(response_data)
    except requests.exceptions.ConnectionError:
        data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.',
            'data': None
        }
        return Response(data)
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)

    
@api_view(['POST'])  
def create_sports(request):
        serializer = SportsSerializer(data=request.data)
        if serializer.is_valid():
            sport_name = serializer.validated_data['sport_name']
            description = serializer.validated_data['description']

            # Validating the name field
            if not sport_name:
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del deporte no puede estar vacío.',
                    'status': False,
                    'data': None
                })

            if not re.match(r'^[a-zA-Z\s]+$', sport_name):
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del deporte solo puede contener letras y espacios.',
                    'status': False,
                    'data': None
                })

            # Validating the description field
            if len(description) > 200:
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'La descripción no puede exceder los 200 caracteres.',
                    'status': False,
                    'data': None
                })

            # Validating duplicate sports
            if Sports.objects.filter(sport_name=sport_name).exists():
                return Response({
                    'code': status.HTTP_200_OK,
                    'message': 'El deporte ya existe en la base de datos.',
                    'status': False,
                    'data': None
                })

            # Save the sports object
            serializer.save()

            return Response({
                'code': status.HTTP_201_CREATED,
                'message': 'Deporte creado exitosamente',
                'status': True,
                'data': None
            })

        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Datos inválidos',
            'status': False,
            'errors': serializer.errors,
            'data': None
        })
    
@api_view(['PUT', 'DELETE'])
def sports_detail(request, pk):
    try:
        try:
            sports = Sports.objects.get(pk=pk)
        except Sports.DoesNotExist:
            return Response(
                data={'code': status.HTTP_200_OK,
                    'message': 'El deporte no existe o ya fue eliminado',
                    'status': False,
                    'data': None
                    }
            )

        if request.method == 'GET':
            serializer = SportsSerializer(sports)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            serializer = SportsSerializer(sports, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response( serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            sports.delete()
            responde_data={
                'code':status.HTTP_204_NO_CONTENT,
                'message':'Deporte eliminado correctamente',
                'status':True,
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