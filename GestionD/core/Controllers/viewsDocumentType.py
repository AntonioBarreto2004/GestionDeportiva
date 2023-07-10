from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializer import *

#DOCUMENTS TYPE
@api_view(['GET']) # METODO GET (LISTAR)
def list_document_types(request):
    queryset = DocumentType.objects.all()
    serializer = DocumentTypeSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_document_type(request):
    serializer = DocumentTypeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'201_CREATED', 'message': 'Usuario creada exitosamente', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_document_type(request, pk):
    try:
        document_type = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = DocumentTypeSerializer(document_type, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Usuario Actualizado exitosamente',  'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_document_type(request, pk):
    try:
        document_type = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    document_type.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Usuario eliminado exitosamente',  'status':True}, status=status.HTTP_204_NO_CONTENT)