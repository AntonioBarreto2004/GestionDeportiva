from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializer import *

#ROLE
@api_view(['GET'])
def list_roles(request):
    queryset = Rol.objects.all()
    serializer = RolSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_role(request):
    serializer = RolSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'201_CREATED', 'message': 'Usuario creada exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_role(request, pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = RolSerializer(role, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Usuario Actualizado exitosamente',  'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_role(request, pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    role.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Usuario eliminado exitosamente',  'status':True}, status=status.HTTP_204_NO_CONTENT)
