import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_instructors(request):
    instructors = Instructors.objects.all()

    instructor_data = []
    for instructor in instructors:
        try:
            user = User.objects.get(people=instructor.people)
            rol_name = user.rol.name_rol if user and user.rol else None
        except User.DoesNotExist:
            rol_name = None

        allergies_data = []
        disabilities_data = []
        special_conditions_data = []

        if instructor.people.peopleallergies_set.exists():
            allergies_data = [
                {
                    'id': allergy.allergies.id,
                    'allergie_name': allergy.allergies.allergie_name,
                    'description': allergy.allergies.description
                }
                for allergy in instructor.people.peopleallergies_set.all()
            ]

        if instructor.people.peopledisabilities_set.exists():
            disabilities_data = [
                {
                    'id': disability.disabilities.id,
                    'disability_name': disability.disabilities.disability_name,
                    'description': disability.disabilities.description
                }
                for disability in instructor.people.peopledisabilities_set.all()
            ]

        if instructor.people.peoplespecialconditions_set.exists():
            special_conditions_data = [
                {
                    'id': condition.specialConditions.id,
                    'specialConditions_name': condition.specialConditions.specialConditions_name,
                    'description': condition.specialConditions.description
                }
                for condition in instructor.people.peoplespecialconditions_set.all()
            ]

        instructor_info = {
            'id': instructor.people.id,
            'name': instructor.people.name,
            'last_name': instructor.people.last_name,
            'rol': rol_name,
            'email': instructor.people.email,
            'photo_user': instructor.people.photo_user.url if instructor.people.photo_user else None,
            'birthdate': instructor.people.birthdate,
            'gender': instructor.people.gender,
            'telephone_number': instructor.people.telephone_number,
            'type_document': instructor.people.type_document_id,
            'num_document': instructor.people.num_document,
            'specialization': instructor.specialization,
            'experience_years': instructor.experience_years,
            'file_documentidentity': instructor.people.file_documentidentity.url if instructor.people.file_documentidentity else None,
            'file_v': instructor.people.file_v.url if instructor.people.file_v else None,
            'file_f': instructor.people.file_f.url if instructor.people.file_f else None,
            'allergies': allergies_data,
            'disabilities': disabilities_data,
            'special_conditions': special_conditions_data,
            'modified_at': instructor.people.modified_at,
        }
        instructor_data.append(instructor_info)

    if not instructor_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se encontraron instructores o personas asociadas',
            'data': []
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Consulta realizada exitosamente',
            'data': instructor_data
        }

    return Response(response_data)



@api_view(['POST'])
def create_instructor(request):
    try:
        # Obtener los datos del cuerpo de la solicitud
        person_id = request.data.get('people')
        specialization = request.data.get('specialization')
        experience_years = request.data.get('experience_years')
        # CreaR una lista para almacenar los campos requeridos faltantes
        campos_faltantes = []
        # Verificar si los campos están vacíos
        if not person_id:
            campos_faltantes.append('people')
        if not specialization:
            campos_faltantes.append('specialization')
        if not experience_years:
            campos_faltantes.append('experience_years')
        # Si hay campos faltantes, devolver la respuesta de error
        if campos_faltantes:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'Los siguientes campos no pueden estar vacios',
                    'data': campos_faltantes
                })
        # Verificar si la persona tiene el rol de instructor
        person = People.objects.get(id=person_id)
        user = User.objects.get(people=person_id)
        if user.rol_id != 2:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'La persona no tiene el rol de instructor.',
                    'data': None
                })
        # Verificar si ya existe un instructor con la misma persona asociada
        if Instructors.objects.filter(people=person).exists():
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'Ya existe un instructor asociado a esta persona.',
                    'data': None
                })
        # Crear el instructor
        instructor = Instructors.objects.create(people=person, specialization=specialization, experience_years=experience_years)
        # Serializar el instructor y devolver la respuesta
        instructor_serializer = InstructorSerializer(instructor)
        return Response(
            data={
                'code': status.HTTP_201_CREATED,
                'status': True,
                'message': 'Instructor creado exitosamente',
                'data': instructor_serializer.data
            })
    except People.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'La persona no existe.',
                'data': None
            })
    except User.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'El usuario no existe.',
                'data': None
            })
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PATCH'])
def update_instructor(request, pk):
    try:
        # Obtener el instructor por su ID
        instructor = Instructors.objects.get(pk=pk)

        # Verificar si la persona tiene el rol de instructor
        user = User.objects.get(people=instructor.people_id)
        if user.rol_id != 2:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': False,
                    'message': 'La persona no tiene el rol de instructor.',
                    'data': None
                })

        # Obtener los datos a actualizar del cuerpo de la solicitud
        specialization = request.data.get('specialization')
        experience_years = request.data.get('experience_years')

        # Actualizar los campos si se proporcionaron en la solicitud
        if specialization:
            instructor.specialization = specialization
        if experience_years:
            instructor.experience_years = experience_years

        # Guardar los cambios en el instructor
        instructor.save()

        # Serializar el instructor actualizado y devolver la respuesta
        instructor_serializer = InstructorSerializer(instructor)
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Instructor actualizado exitosamente',
                'data': instructor_serializer.data
            })

    except Instructors.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'El instructor no existe.',
            })

    except User.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': False,
                'message': 'El usuario no existe.',
            })

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)
    

@api_view(['DELETE'])
def delete_instructor(request, pk):
    try:
        try:
        # Verificar si el instructor existe
            instructor = Instructors.objects.get(pk=pk)
        except Instructors.DoesNotExist:
            responde_data = {
                'code': status.HTTP_200_OK,
                'message': 'Instructor no existente',
                'status': False,
                'data': None
            }
            return Response(responde_data)
        
        # Eliminar el instructor
        instructor.delete()
        # Devolver la respuesta
        return Response(
            data={
                'code': status.HTTP_200_OK, 
                'status': True, 
                'message': 'Instructor eliminado exitosamente',
            }
        )

    except Exception as e:
        data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)