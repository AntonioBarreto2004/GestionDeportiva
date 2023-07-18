from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from ..models import *


@api_view(['GET'])
def get_servicio(request):
    # Aplicar filtros si se proporcionan parámetros de consulta
    nombre_servicio = request.query_params.get('nombre_servicio')
    descripcion_servicio = request.query_params.get('descripcion_servicio')
    
    servicios = Servicio.objects.all()
    
    # Filtrar por nombre del servicio
    if nombre_servicio:
        servicios = servicios.filter(nombreServicio__icontains=nombre_servicio)
    
    # Filtrar por descripción del servicio
    if descripcion_servicio:
        servicios = servicios.filter(DescripcionServicio__icontains=descripcion_servicio)
    
    serializer = ServicioSerializer(servicios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_servicio(request):
    serializer = ServicioSerializer(data=request.data)
    if serializer.is_valid():
        # Validar el valor del servicio
        valor_servicio = serializer.validated_data.get('ValorServicio')
        if valor_servicio <= 0:
            return Response({'message': 'El valor del servicio debe ser mayor que cero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_servicio(request, pk):
    try:
        servicio = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ServicioSerializer(servicio, data=request.data, partial=True)
    if serializer.is_valid():
        # Validar el valor del servicio
        valor_servicio = serializer.validated_data.get('ValorServicio')
        if valor_servicio <= 0:
            return Response({'message': 'El valor del servicio debe ser mayor que cero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_servicio(request, pk):
    try:
        servicio = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    servicio.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
