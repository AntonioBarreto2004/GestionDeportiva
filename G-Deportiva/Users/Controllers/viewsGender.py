from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_genders(request):
    queryset = gender.objects.all()
    serializer = GenderSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_gender(request):
    serializerG = GenderSerializer(data=request.data)
    serializerG.is_valid(raise_exception=True)
    validated_data = serializerG.validated_data

    # Realizar verificación adicional para evitar datos duplicados
    if gender.objects.filter(name_gender=validated_data['name_gender']).exists():
        return Response(data={'code': '409_CONFLICT', 'message': 'Los datos ya existen', 'status': False}, status=status.HTTP_409_CONFLICT)

    serializerG.save()
    return Response(data={'code': '201_CREATED', 'message': 'Género creado exitosamente', 'status': True}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_gender(request, pk):
    try:
        gender_instance = gender.objects.get(pk=pk)
    except gender.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'El género no existe', 'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializerEg = GenderSerializer(gender_instance, data=request.data, partial=True)
    serializerEg.is_valid(raise_exception=True)
    serializerEg.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Género actualizado exitosamente', 'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_gender(request, pk):
    try:
        gender_instance = gender.objects.get(pk=pk)
    except gender.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'El género no existe', 'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    gender_instance.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Género eliminado exitosamente', 'status':True}, status=status.HTTP_204_NO_CONTENT)
