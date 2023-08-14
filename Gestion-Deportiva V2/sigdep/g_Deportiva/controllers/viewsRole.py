from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

#ROLE
@api_view(['GET'])
def list_roles(request):
    queryset = Rol.objects.all()
    if queryset.exists():
        serializer = RolSerializer(queryset, many=True)
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos encontrados',
            'data': serializer.data
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No hay datos',
            'data': None
        }

    return Response(response_data)

@api_view(['POST'])
def create_role(request):
    serializerR = RolSerializer(data=request.data)
    serializerR.is_valid(raise_exception=True)
    validated_data = serializerR.validated_data

    # Realizar verificación adicional para evitar datos duplicados
    if Rol.objects.filter(name_rol=validated_data['name_rol']).exists():
        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Los datos ya existen', 
                              'status': False})

    serializerR.save()
    return Response(
                data={'code': status.HTTP_201_CREATED, 
                'message': 'Rol creado exitosamente', 
                'status': True})

@api_view(['PATCH'])
def update_role(request, pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 
                              'message': 'Rol no existe',  
                              'status':False})
    
    name_rol = request.data.get('name_rol')

    existing_sport = Rol.objects.filter(name_rol=name_rol).first()
    if existing_sport:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Ya existe un Rol con el mismo nombre.',
                'data': None
            })
    
    serializerE = RolSerializer(role, data=request.data, partial=True)
    serializerE.is_valid(raise_exception=True)
    serializerE.save()
    return Response(data={'code':status.HTTP_200_OK, 
                          'message': 'Rol Actualizado exitosamente',  
                          'status':True})

@api_view(['DELETE'])
def delete_role(pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 
                              'message': 'Rol no existe',  
                              'status':False})
    
    role.delete()
    return Response(data={'code':status.HTTP_200_OK, 
                          'message': 'Rol eliminado exitosamente',  
                          'status':True})