import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_sports(request):
    try:
        id = request.GET.get('id')
        sport_name = request.GET.get('sport_name')
        creation_date = request.GET.get('creation_date')

        queryset = Sports.objects.all().order_by('id')

        if id:
            queryset = queryset.filter(id=id)
        if sport_name:
            queryset = queryset.filter(sport_name=sport_name)
        if creation_date:
            queryset = queryset.filter(creation_date=creation_date)

        if not queryset.exists():
            return Response(
                data = { 
                    'code': status.HTTP_200_OK, 
                    'message': 'No se encontraron datos existentes', 
                    'status': False,
                    'data': None,
                }
            )

        sports_data = []
        for sport in queryset:
            categories = Category.objects.filter(categorysport__sport_id=sport.id)
            category_data = [
                {
                    'id': category.id,
                    'category_name': category.category_name,
                    'description': category.description
                }
                for category in categories
            ]

            sport_data = {
                'id': sport.id,
                'sport_name': sport.sport_name,
                'description': sport.description,
                'categories': category_data
            }
            sports_data.append(sport_data)

        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Datos Encontrados',
            'data': sports_data
        }
        return Response(response_data)
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)




    
@api_view(['POST'])
def create_sports(request):
    serializer = SportsSerializer(data=request.data)
    if serializer.is_valid():
        sport_name = serializer.validated_data['sport_name']
        description = serializer.validated_data['description']
        category_ids = [category['id'] for category in request.data.get('category_ids', [])]

        # Validating the name field
        if not sport_name:
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Nombre del deporte no puede estar vacío.',
                'status': False,
                'data': None
            })

        # Validating the description field
        if len(description) > 200:
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'La descripción no puede exceder los 200 caracteres.',
                'status': False,
                'data': None
            })

        # Validating duplicate sports
        if Sports.objects.filter(sport_name=sport_name).exists():
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'El deporte ya existe en la base de datos.',
                'status': False,
                'data': None
            })

        # Save the sports object
        sport = serializer.save()

        # Associate the sport with categories if category_ids are provided
        if category_ids:
            associated_categories = []
            for category_id in category_ids:
                try:
                    category = Category.objects.get(pk=category_id)
                    CategorySport.objects.get_or_create(category_id=category, sport_id=sport)
                    associated_categories.append(category.category_name)
                except Category.DoesNotExist:
                    pass

            return Response({
                'code': status.HTTP_201_CREATED,
                'message': 'Deporte creado exitosamente',
                'status': True,
                'associated_categories': f'categorias asociadas {associated_categories}'
            })
        else:
            return Response({
                'code': status.HTTP_201_CREATED,
                'message': 'Deporte creado exitosamente',
                'status': True,
                'associated_categories': 'No se han asociado categorías'
            })
    else:
        return Response({
            'code': status.HTTP_200_OK,
            'message': 'Error al crear el deporte',
            'status': True,
            'data': serializer.errors
        })
    
@api_view(['PATCH'])
def update_sport(request, pk):
    try:
        sport = Sports.objects.get(pk=pk)
    except Sports.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'El deporte no existe',
                'data': None
            })

    # Obtener los campos de la solicitud
    sport_name = request.data.get('sport_name')
    description = request.data.get('description')
    category_ids = request.data.get('category_ids', [])

    campos_faltantes = []
    # Verificar si los campos están vacíos
    if not sport_name:
        campos_faltantes.append('sport_name')
    if not description:
        campos_faltantes.append('description')
    if campos_faltantes:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Los siguientes campos no pueden estar vacios',
                'data': campos_faltantes
            })

    # Verificar si el deporte ya existe con el mismo nombre
    existing_sport = Sports.objects.filter(sport_name=sport_name).exclude(pk=pk).first()
    if existing_sport:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'Ya existe un deporte con el mismo nombre.',
                'data': None
            })

    # Actualizar los campos del deporte
    sport.sport_name = sport_name
    sport.description = description
    sport.save()

    # Eliminar relaciones con categorías existentes
    sport.categorysport_set.filter(category_id__in=[item['id'] for item in category_ids]).delete()

    # Agregar nuevas relaciones con categorías
    for category_id in category_ids:
        category = Category.objects.get(pk=category_id['id'])
        CategorySport.objects.create(category_id=category, sport_id=sport)

    responde_data = {
        'code': status.HTTP_200_OK,
        'message': 'Deporte actualizado exitosamente',
        'status': True,
        'data': None
    }
    return Response(responde_data)


@api_view(['DELETE'])
def delete_sport(request, pk):
    try:
        sport = Sports.objects.get(pk=pk)
    except Sports.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'El deporte no existe',
                'data': None
            })
    sport.delete()

    response_data = {
        'code': status.HTTP_200_OK,
        'message': 'Deporte eliminado correctamente',
        'status': True,
        'data': None
    }

    return Response(response_data)

    

@api_view(['POST'])
def state_sport(request):
    try:
        # Obtener los datos del cuerpo de la solicitud
        sport_id = request.data.get('sport_id')
        action = request.data.get('action')

        campos_faltantes = []
        # Verificar si los campos están vacíos
        if not sport_id:
            campos_faltantes.append('"sport_id": id del Deporte existente')
        if not action:
            campos_faltantes.append('"action": Debe proporcionar un valor (activate o desactivate).')

        if campos_faltantes:
            # Si el campo "action" está vacío, devolver una respuesta informando que debe proporcionar un valor
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'Debe proporcionar un valor en los campos',
                    'data': campos_faltantes
                })
        # Verificar si el deporte existe
        try:
            sport = Sports.objects.get(id=sport_id)
        except Sports.DoesNotExist:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'El deporte no existe.',
                    'data': None
                })
        # Realizar la acción según el valor de "action"
        if action == "desactivate":
            # Desactivar el deporte si aún está activo
            if sport.sport_status:
                sport.sport_status = False
                sport.save()
                message = 'Deporte desactivado exitosamente.'
            else:
                message = 'El deporte ya está desactivado.'

        elif action == "activate":
            # Activar el deporte si está desactivado
            if not sport.sport_status:
                sport.sport_status = True
                sport.save()
                message = 'Deporte activado exitosamente.'
            else:
                message = 'El deporte ya está activado.'

        else:
            # Si se proporciona un valor incorrecto para "action"
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'El valor del campo "action" es incorrecto. Debe ser "activate" o "desactivate".',
                    'data': None
                })

        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': True,
                'message': message,
                'data': None
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)