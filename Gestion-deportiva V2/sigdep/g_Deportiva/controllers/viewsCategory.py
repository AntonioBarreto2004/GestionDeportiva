from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_category(request):
    try:
        list_category = Category.objects.all()
        if not list_category:
            responde_data = {
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'No hay datos registrados',
                'data': None
            }
            return Response(responde_data)
    
        serializer_ctg = CategorySerializer(list_category, many=True)
        responde_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos encontrados',
            'data': serializer_ctg.data
        }
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)
    
@api_view(['POST'])
def create_category(request):
    category_create = CategorySerializer(data=request.data)
    category_create.is_valid(raise_exception=True)