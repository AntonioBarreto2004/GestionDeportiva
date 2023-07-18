from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

#ROLE
@api_view(['GET'])
def list_roles(request):
    queryset = Rol.objects.all()
    serializer = RolSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_role(request):
    serializerR = RolSerializer(data=request.data)
    serializerR.is_valid(raise_exception=True)
    validated_data = serializerR.validated_data

    # Realizar verificación adicional para evitar datos duplicados
    if Rol.objects.filter(name_rol=validated_data['name_rol']).exists():
        return Response(data={'code': '409_CONFLICT', 'message': 'Los datos ya existen', 'status': False}, status=status.HTTP_409_CONFLICT)

    serializerR.save()
    return Response(data={'code': '201_CREATED', 'message': 'Rol creado exitosamente', 'status': True}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_role(request, pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Rol no existe',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializerE = RolSerializer(role, data=request.data, partial=True)
    serializerE.is_valid(raise_exception=True)
    serializerE.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Rol Actualizado exitosamente',  'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_role(pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Rol no existe',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    role.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Rol eliminado exitosamente',  'status':True}, status=status.HTTP_204_NO_CONTENT)