from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

#DOCUMENTS TYPE
@api_view(['GET']) # METODO GET (LISTAR)
def list_document_types(request):
    queryset = DocumentType.objects.all()
    serializer = DocumentTypeSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_document_type(request):
    serializerD = DocumentTypeSerializer(data=request.data)
    serializerD.is_valid(raise_exception=True)
    validated_data = serializerD.validated_data

    # Realizar verificación adicional para evitar datos duplicados
    if DocumentType.objects.filter(name=validated_data['name']).exists():
        return Response(data={'code': '409_CONFLICT', 'message': 'Los datos ya existen', 'status': False}, status=status.HTTP_409_CONFLICT)

    serializerD.save()
    return Response(data={'code': '201_CREATED', 'message': 'Tipo de Documento creado exitosamente', 'status': True}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_document_type(request, pk):
    try:
        document_type = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Tipo de Documento no existe',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializerUt = DocumentTypeSerializer(document_type, data=request.data, partial=True)
    serializerUt.is_valid(raise_exception=True)
    serializerUt.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Tipo de Documento Actualizado exitosamente',  'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_document_type(request, pk):
    try:
        document_type = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Tipo de Documento no existe',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    document_type.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Tipo de Documento eliminado exitosamente',  'status':True}, status=status.HTTP_204_NO_CONTENT)