from datetime import datetime
import re
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Sports
from django_filters import rest_framework as filters
from ..serializer import SportsSerializer
from django.db import IntegrityError

@api_view(['GET'])
def list_sports(request):
    try:
        id = request.GET.get('id')
        name = request.GET.get('name')
        creation_date = request.GET.get('creation_date')

        queryset = Sports.objects.all()

        if id:
            queryset = queryset.filter(id=id)
        if name:
            queryset = queryset.filter(name=name)
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
    try:
        serializer = SportsSerializer(data=request.data)
        if serializer.is_valid():
            # Validating the name field
            name = serializer.validated_data['name']
            if not name:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del deporte no puede estar vacío.',
                    'status': False
                }
                return Response(response_data)
            elif not re.match(r'^[a-zA-Z\s]+$', name):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del deporte solo puede contener letras y espacios.',
                    'status': False
                }
                return Response(response_data)
            
            elif not name.isalpha():
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Nombre del deporte solo puede contener letras.',
                    'status': False
                }
                return Response(response_data)

            # Validating the description field
            description = serializer.validated_data['description']
            if len(description) > 250:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'La descripción no puede exceder los 250 caracteres.',
                    'status': False
                }
                return Response(response_data)

            # Validating duplicate sports
            if Sports.objects.filter(name=name).exists():
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'El deporte ya existe en la base de datos.',
                    'status': False
                }
                return Response(response_data)

            # Save the sports object
            serializer.save()
            
            response_data = {
                'code': status.HTTP_201_CREATED,
                'message': 'Deporte creado exitosamente',
                'status': True,
                'data': None
            }
            return Response(response_data)

        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Datos invalidos',
            'status': False,
            'errors': serializer.errors
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
    

@api_view(['PATCH'])
def update_sport(request, pk):
    try:
        try:
            p_sport = Sports.objects.get(pk=pk)
        except Sports.DoesNotExist:
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': 'Deporte no existente',
                'status': False,
                'data': None
            }
            return Response(responde_data)
        
        p_sport = SportsSerializer(Sports, data=request.data, partial=True)
        p_sport.is_valid(raise_exception=True)
        p_sport.save()

        response_data ={
            'code': status.HTTP_200_OK,
            'message': 'Deporte actualizado exitosamente',
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
    
@api_view(['DELETE'])
def delete_sport(request, pk):
    try:
        try:
            sport = Sports.objects.get(pk=pk)
        except Sports.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Deporte no encontrado.', 
                                'status': False,
                                'data':None
                                }, 
                    
                            )

        name_sport = Sports.name
        sport.delete()
        
        response_data ={
            'code': status.HTTP_200_OK,
            'message': f'Datos de {name_sport} eliminados exitosamente',
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