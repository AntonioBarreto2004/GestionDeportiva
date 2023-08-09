import requests
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from ..serializers import *
from ..models import *


#ATHLETE

        #METODO GET (LISTAR)
@api_view(['GET'])
def list_athlete(request):
    athletes = Athlete.objects.all()

    athlete_data = []
    for athlete in athletes:
        try:
            user = User.objects.get(people=athlete.people)
            rol_name = user.rol.name_rol if user and user.rol else None
        except User.DoesNotExist:
            rol_name = None

        allergies_data = []
        disabilities_data = []
        special_conditions_data = []

        if athlete.people.peopleallergies_set.exists():
            allergies_data = [
                {
                    'id': allergy.allergies.id,
                    'allergie_name': allergy.allergies.allergie_name,
                    'description': allergy.allergies.description
                }
                for allergy in athlete.people.peopleallergies_set.all()
            ]

        if athlete.people.peopledisabilities_set.exists():
            disabilities_data = [
                {
                    'id': disability.disabilities.id,
                    'disability_name': disability.disabilities.disability_name,
                    'description': disability.disabilities.description
                }
                for disability in athlete.people.peopledisabilities_set.all()
            ]

        if athlete.people.peoplespecialconditions_set.exists():
            special_conditions_data = [
                {
                    'id': condition.specialConditions.id,
                    'specialConditions_name': condition.specialConditions.specialConditions_name,
                    'description': condition.specialConditions.description
                }
                for condition in athlete.people.peoplespecialconditions_set.all()
            ]

        athlete_info = {
            'id': athlete.people.id,
            'name': athlete.people.name,
            'last_name': athlete.people.last_name,
            'rol': rol_name,
            'email': athlete.people.email,
            'sport': athlete.sports.sport_name,
            'photo_user': athlete.people.photo_user.url if athlete.people.photo_user else None,
            'birthdate': athlete.people.birthdate,
            'gender': athlete.people.gender,
            'telephone_number': athlete.people.telephone_number,
            'type_document_id': athlete.people.type_document_id,
            'num_document': athlete.people.num_document,
            'file_documentidentity': athlete.people.file_documentidentity.url if athlete.people.file_documentidentity else None,
            'file_v': athlete.people.file_v.url if athlete.people.file_v else None,
            'file_f': athlete.people.file_f.url if athlete.people.file_f else None,
            'allergies': allergies_data,
            'disabilities': disabilities_data,
            'special_conditions': special_conditions_data,
            'modified_at': athlete.people.modified_at,
            
        }
        athlete_data.append(athlete_info)

    if not athlete_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se encontraron deportistas o personas asociadas',
            'data': []
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Consulta realizada exitosamente',
            'data': athlete_data
        }

    return Response(response_data)



    
@api_view(['POST'])
def create_athlete(request):
    data = request.data
    atleta_data = data.get('people')

    empty_fields = []

    required_fields = ['people', 'instructor', 'technicalv', 'tacticalv', 'physicalv', 'sports']

    for field in required_fields:
        if field not in data or data[field] == "":
            empty_fields.append(field)

    if empty_fields:
        response_data = {
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'Los siguientes campos son requeridos o están vacíos:',
            'data': format(', '.join(empty_fields))
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    person_id = data['people']
    person_id = request.data.get('people')

    if Athlete.objects.filter(people_id=person_id).exists():
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Ya existe un Atleta asociado a esta persona.',
            'status': False,
            'data': None
        }
        return Response(response_data)
    
    try:
        person = People.objects.get(id=person_id)
        user = User.objects.get(people=person)
        print("Rol del usuario:", user.rol)
        if user.rol.name_rol != "Atleta":
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'La persona no tiene el rol de Atleta.',
                    'data': None
                }
            )
    except People.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_400_BAD_REQUEST,
                'status': False,
                'message': 'La persona no existe.',
                'data': None
            }
        )
    
    instructor_id = request.data.get('instructor')
    if not instructor_id:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'El campo instructor es requerido.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        instructor = Instructors.objects.get(id=instructor_id)
    except Instructors.DoesNotExist:
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'status': False,
            'message': 'Instructor no encontrado.',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AthleteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(instructor=instructor)  # Establecer el objeto instructor en lugar del ID

    response_data = {
        'code': status.HTTP_201_CREATED,
        'message': 'Atleta registrado exitosamente',
        'status': True,
        'data': None
    }
    return Response(response_data)



@api_view(['PATCH'])
def update_athlete(request, pk):
    try:
        try:
            athlete = Athlete.objects.get(pk=pk)
        except Athlete.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Atleta no encontrado.', 
                                'status': False,
                                'data':None
                                },
                            )
        
        serializer = AthleteSerializer(athlete, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response_data ={
            'code': status.HTTP_200_OK,
            'message': f'Datos de {athlete.people.name} actualizados exitosamente',
            'status': True,
            'data': None
        }
        return Response(response_data)
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)



@api_view(['DELETE'])
def delete_athlete(request, pk):
    try:
        try:
            athlete = Athlete.objects.get(pk=pk)
        except Athlete.DoesNotExist:
            return Response(data={'code': status.HTTP_200_OK, 
                                'message': 'Atleta no encontrado.', 
                                'status': False,
                                'data':None
                                }, 
                    
                            )

        athlete_name = athlete.people.name
        athlete.delete()
        
        response_data ={
            'code': status.HTTP_204_NO_CONTENT,
            'message': f'Datos de {athlete_name} eliminados exitosamente',
            'status': True,
            'data': None
        }
        return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)
    except requests.exceptions.ConnectionError:
        data={
            'code': status.HTTP_400_BAD_REQUEST,
            'status': False,
            'message': 'La URL se ha perdido. Por favor, inténtalo más tarde.', 
            'data': None
                  }
        return Response(data)
    
    except Exception as e:
        data= {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False, 
            'message': 'Error del servidor',
            'data': None
                    }
        return Response(data)
    
    
@api_view(['POST'])
def state_atlete(request):
    try:
        # Obtener los datos del cuerpo de la solicitud
        Athlete_id = request.data.get('Athlete_id')
        action = request.data.get('action')

        campos_faltantes = []
        # Verificar si los campos están vacíos
        if not Athlete_id:
            campos_faltantes.append('"Athlete_id": id del Atleta existente')
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
        # Verificar si el Atleta existe
        try:
            athlete = Athlete.objects.get(id=Athlete_id)
        except Athlete.DoesNotExist:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'El Atleta no existe.',
                    'data': None
                })
        # Realizar la acción según el valor de "action"
        if action == "desactivate":
            # Desactivar el Atleta  si aún está activo
            if athlete.athlete_status:
                athlete.athlete_status = False
                athlete.save()
                message = 'Atleta desactivado exitosamente.'
            else:
                message = 'El Atleta ya está desactivado.'

        elif action == "activate":
            # Activar el deporte si está desactivado
            if not athlete.athlete_status:
                athlete.athlete_status = True
                athlete.save()
                message = 'Atleta activado exitosamente.'
            else:
                message = 'El Atleta  ya está activado.'

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