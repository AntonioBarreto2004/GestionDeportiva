from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..serializers import *
from ..models import *


@api_view(['GET'])
def get_recibo_pago(request):
    # Aplicar filtros si se proporcionan parámetros de consulta
    fecha_pago = request.query_params.get('fecha_pago')
    
    recibos_pago = ReciboPago.objects.all()
    
    # Filtrar por fecha de pago
    if fecha_pago:
        recibos_pago = recibos_pago.filter(fechaPago=fecha_pago)
    
    serializer = ReciboPagoSerializer(recibos_pago, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_recibo_pago(request):
    serializer = ReciboPagoSerializer(data=request.data)
    if serializer.is_valid():
        # Validar el valor del pago
        valor_pago = serializer.validated_data.get('ValorPago')
        if valor_pago <= 0:
            return Response({'message': 'El valor del pago debe ser mayor que cero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_recibo_pago(request, pk):
    try:
        recibo_pago = ReciboPago.objects.get(pk=pk)
    except ReciboPago.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReciboPagoSerializer(recibo_pago, data=request.data, partial=True)
    if serializer.is_valid():
        # Validar el valor del pago
        valor_pago = serializer.validated_data.get('ValorPago')
        if valor_pago <= 0:
            return Response({'message': 'El valor del pago debe ser mayor que cero.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_recibo_pago(request, pk):
    try:
        recibo_pago = ReciboPago.objects.get(pk=pk)
    except ReciboPago.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    recibo_pago.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
