from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Sports
from django_filters import rest_framework as filters
from ..serializer import SportsSerializer

@api_view(['GET'])
def list_sports(request):
    class sportsFilter(filters.FilterSet):
        class Meta:
            model = Sports
            fields = {
            'id': ['exact', 'icontains'],
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'creation_date': ['exact', 'year__gt', 'year__lt'],
        }

    queryset = Sports.objects.all()
    sports_filter = sportsFilter(request.query_params, queryset=queryset)
    filtered_queryset = sports_filter.qs

    if not filtered_queryset.exists():
        return Response(
            data={'code': '404_NOT_FOUND', 'message': 'Usuario no existe', 'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = SportsSerializer(filtered_queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_sports(request):
    serializer = SportsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sports_detail(request, pk):
    try:
        sports = Sports.objects.get(pk=pk)
    except Sports.DoesNotExist:
        return Response(
            data={'code': '404_NOT_FOUND',
                  'message': 'El deporte no existe',
                  'status': False},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = SportsSerializer(sports)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SportsSerializer(sports, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sports.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
