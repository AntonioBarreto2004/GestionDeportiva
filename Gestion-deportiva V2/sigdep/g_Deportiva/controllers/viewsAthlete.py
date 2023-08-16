import re
import requests
from rest_framework import status
from django.conf import settings
from django.db import transaction
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from ..serializers import *
from ..models import *

@api_view(['GET'])
def list_athlete(request):
    athletes = Athlete.objects.all()

    athlete_data = []
    for athlete in athletes:
        try:
            user = User.objects.get(people=athlete.people)
            rol_name = user.rol.name if user and user.rol else None
        except User.DoesNotExist:
            rol_name = None

        allergies_data = []
        disabilities_data = []
        special_conditions_data = []

        if athlete.people.peopleallergies_set.exists():
            allergies_data = [
                {
                    'id': allergy.allergies.id,
                    'name': allergy.allergies.name,
                    'description': allergy.allergies.description
                }
                for allergy in athlete.people.peopleallergies_set.all()
            ]

        if athlete.people.peopledisabilities_set.exists():
            disabilities_data = [
                {
                    'id': disability.disabilities.id,
                    'name': disability.disabilities.name,
                    'description': disability.disabilities.description
                }
                for disability in athlete.people.peopledisabilities_set.all()
            ]

        if athlete.people.peoplespecialconditions_set.exists():
            special_conditions_data = [
                {
                    'id': condition.specialconditions.id,
                    'name': condition.specialconditions.name,
                    'description': condition.specialconditions.description
                }
                for condition in athlete.people.peoplespecialconditions_set.all()
            ]
        
        birthdate = athlete.people.birthdate
        age = relativedelta(datetime.now().date(), birthdate).years

        athlete_info = {
            'id': athlete.id,
            'name': f"{athlete.people.name} {athlete.people.last_name}",
            'rol': rol_name,
            'email': athlete.people.email,
            'instructor': f"{athlete.instructor.people.name} {athlete.instructor.people.last_name}" if athlete.instructor else None,
            'sport': athlete.sports.name,
            'photo_user': athlete.people.photo_user,
            'birthdate': athlete.people.birthdate,
            'age': age,
            'gender': athlete.people.gender,
            'telephone_number': athlete.people.telephone_number,
            'type_document': athlete.people.type_document,
            'num_document': athlete.people.num_document,
            'technicalv': athlete.technicalv,
            'tacticalv': athlete.tacticalv,
            'physicalv': athlete.physicalv,
            'file_documentidentity': athlete.people.file_documentidentity,
            'file_eps_certificate': athlete.people.file_eps_certificate,
            'file_informed_consent': athlete.people.file_informed_consent,
            'allergies': allergies_data,
            'disabilities': disabilities_data,
            'special_conditions': special_conditions_data,
            'modified_at': athlete.people.modified_at,
        }
        athlete_data.append(athlete_info)

    if not athlete_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No se encuentran datos de atletas.',
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


def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/correo.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$')
    
@api_view(['POST'])
def create_athlete(request):
    with transaction.atomic():
        # Obtener los datos del cuerpo de la solicitud
        person_data = request.data.get('people')
        instructor_id = request.data.get('instructor')
        technicalv = request.data.get('technicalv')
        tacticalv = request.data.get('tacticalv')
        physicalv = request.data.get('physicalv')
        sport_id = request.data.get('sports')

        # Validar que las valoraciones estén dentro del rango de 1 a 5
        def validate_rating(rating):
            try:
                rating = int(rating)
                if rating < 1:
                    return 1
                elif rating > 5:
                    return 5
                return rating
            except ValueError:
                return 1

        technicalv = validate_rating(technicalv)
        tacticalv = validate_rating(tacticalv)
        physicalv = validate_rating(physicalv)

        # Validar que los campos requeridos no estén vacíos
        empty_fields = []
        required_fields = ['email', 'name', 'last_name', 'num_document', 'birthdate', 
                           'telephone_number', 'type_document', 'gender']
        for field in required_fields:
            if not person_data.get(field):
                empty_fields.append(field)

        if empty_fields:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'Los siguientes campos no pueden estar vacíos',
                    'status': True,
                    'data': f'{empty_fields}'
                })

        # Realizar verificación adicional para evitar usuarios duplicados
        email = person_data['email']
        num_document = person_data['num_document']
        # Validate email format
        if not EMAIL_REGEX.match(email):
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'El formato del correo electrónico es inválido.',
                    'data': None
                })
        if People.objects.filter(email=email).exists():
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'Ya existe una persona con este correo registrado',
                    'status': True,
                    'data': None
                })

        if People.objects.filter(num_document=num_document).exists():
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'message': 'Ya existe un usuario con este número de documento',
                    'status': True,
                    'data': None
                })

        # Validar nombre y apellido
        name = person_data['name']
        last_name = person_data['last_name']
        type_document = person_data['type_document']
        phone_number = person_data['telephone_number']

        if not re.match(r'^[a-zA-Z\s]+$', name) or not re.match(r'^[a-zA-Z\s]+$', last_name):
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'El nombre y apellido del usuario solo pueden contener letras y espacios.',
                'status': True
            }
            return Response(response_data)

        # Validar el número de documento
        if not re.fullmatch(r'^\d{8,10}$', str(num_document)):
            response_data = {
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'El número de documento debe tener entre 8 y 10 dígitos.',
                'data': None
            }
            return Response(response_data)
        
        if not re.match(r'^[a-zA-Z\s]+$', type_document):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'El Tipo de documento solo pueden contener letras y espacios.',
                    'status': True
                }
                return Response(response_data)

        if not re.match(r'^\d{10}$', phone_number):
            response_data = {
                'code': status.HTTP_200_OK,
                'message':'El numero telefonico solo puede contener 10 Digitos y Ninguna letra',
                'status': True
            }
            return Response(response_data)

        people_serializer = PeopleSerializer(data=person_data)
        if people_serializer.is_valid():
            person = people_serializer.save()
        else:
            person.delete()
            response_data = {
                'data': status.HTTP_200_OK,
                'status': True,
                'message': 'Error en la creacion.',
                'data': None
            }
            return Response(response_data)
        
        # Crear el atleta
        Athlete.objects.create(
            people=person,
            technical=person_data.get('technical'),
            tactical=person_data.get('tactical'),
            physical=person_data.get('physical'),
        )

        # Buscar el rol "Atleta" en la base de datos y asignarlo al usuario
        try:
            athlete_role = Rol.objects.get(name='Atleta')
        except Rol.DoesNotExist:
            return Response(
                data={
                    'code': status.HTTP_200_OK,
                    'status': True,
                    'message': 'El rol "Atleta" no existe.',
                    'data': None
                })
        # Obtener el número de documento y convertirlo en cadena
        document_number = str(num_document)  # Convertir el número de documento a cadena
        generated_password = document_number  # Usar la cadena del número de documento como contraseña
  # Generar contraseña basada en el número de documento

        # Crear el usuario y asignar el rol de Atleta
        User.objects.create(
            people=person,
            rol=athlete_role,
            password=make_password(generated_password),  # Aplicar el hash a la contraseña
            is_active=True
        )

        # Manejar las relaciones muchos a muchos
        if 'allergies' in person_data:
            allergies_ids = [allergy['id'] for allergy in person_data['allergies']]
            allergies_associated = Allergies.objects.filter(id__in=allergies_ids)
            for allergy in allergies_associated:
                peopleallergies.objects.create(people=person, allergies=allergy)

        if 'disabilities' in person_data:
            disabilities_ids = [disability['id'] for disability in person_data['disabilities']]
            disabilities_associated = Disabilities.objects.filter(id__in=disabilities_ids)
            for disability in disabilities_associated:
                peopleDisabilities.objects.create(people=person, disabilities=disability)

        if 'special_conditions' in person_data:
            special_conditions_ids = [condition['id'] for condition in person_data['special_conditions']]
            special_conditions_associated = specialconditions.objects.filter(id__in=special_conditions_ids)
            for condition in special_conditions_associated:
                peoplespecialConditions.objects.create(people=person, specialconditions=condition)

        # Manejar las relaciones muchos a muchos (allergies, disabilities, special_conditions)
        send_activation_email(person.name, person.email, generated_password)

        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'Registro se ha realizado con éxito.',
                'data': None
            })



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
        people_data = request.data.get('people')
        if people_data:
            serializerPd = PeopleSerializer(athlete.people, data=people_data, partial=True)
            serializerPd.is_valid(raise_exception=True)
            serializerPd.save()  # Actualiza los datos de People

        name = people_data.get('name') if people_data else None
        last_name = people_data.get('last_name') if people_data else None

        if name and not re.match(r'^[a-zA-Z\s]+$', name):
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Nombre de la persona solo puede contener letras y espacios.',
                'status': False
            }
            return Response(response_data)

        if last_name and not re.match(r'^[a-zA-Z\s]+$', last_name):
            response_data = {
                'code': status.HTTP_200_OK,
                'message': 'Apellido de la persona solo puede contener letras y espacios.',
                'status': False
            }
            return Response(response_data)
        
        # Manejar campos de archivo si se proporcionan en la solicitud
        if 'photo_user' in request.FILES:
            athlete.people.photo_user = request.FILES['photo_user']
        else:
            athlete.people.photo_user = None
        if 'file_documentidentity' in request.FILES:
            athlete.people.file_documentidentity = request.FILES['file_documentidentity']
        else:
            athlete.people.file_documentidentity = None
        if 'file_EPS_certificate' in request.FILES:
            athlete.people.file_eps_certificate = request.FILES['file_eps_certificate']
        else:
            athlete.people.file_eps_certificate = None
        if 'file_informed_consent' in request.FILES:
            athlete.people.file_informed_consent = request.FILES['file_informed_consent']
        else:
            athlete.people.file_informed_consent = None
        # ... manejar otros campos de archivo ...
        
        technicalv = request.data.get('technicalv')
        tacticalv = request.data.get('tacticalv')
        physicalv = request.data.get('physicalv')

        # Validar que las valoraciones estén dentro del rango de 1 a 5
        def validate_rating(rating):
            try:
                rating = int(rating)
                if rating < 1:
                    return 1
                elif rating > 5:
                    return 5
                return rating
            except ValueError:
                return 1
        
        if technicalv:
            athlete.technicalv = validate_rating(technicalv)
        if tacticalv:
            athlete.tacticalv = validate_rating(tacticalv)
        if physicalv:
            athlete.physicalv = validate_rating(physicalv)

        # Actualizar llave foránea 'instructor' si se proporciona
        instructor_id = request.data.get('instructor')
        if instructor_id is not None:
            try:
                instructor = Instructors.objects.get(pk=instructor_id)
                athlete.instructor = instructor
            except Instructors.DoesNotExist:
                return Response(data={
                    'code': status.HTTP_200_OK,
                    'message': f'Instructor con ID {instructor_id} no encontrado.',
                    'status': False,
                    'data': None,
                })

        # Actualizar llave foránea 'sports' si se proporciona
        sport_id = request.data.get('sports')
        if sport_id is not None:
            try:
                sports_instance = Sports.objects.get(pk=sport_id)
                athlete.sports = sports_instance
            except Sports.DoesNotExist:
                return Response(data={
                    'code': status.HTTP_200_OK,
                    'message': f'Deporte con ID {sport_id} no encontrado.',
                    'status': False,
                    'data': None,
                })

        # Actualizar alergias, discapacidades y condiciones especiales
        allergies = request.data.get('allergies', [])
        disabilities = request.data.get('disabilities', [])
        special_conditions = request.data.get('special_conditions', [])

        with transaction.atomic():  # Utilizar una transacción para las operaciones de relación
            if allergies:  # Verificar si hay alergias para actualizar
                athlete.people.peopleallergies_set.all().delete()
                for allergy_data in allergies:
                    allergy_id = allergy_data.get('id')
                    try:
                        allergy = Allergies.objects.get(id=allergy_id)
                        peopleallergies.objects.create(people=athlete.people, allergies=allergy)
                    except Allergies.DoesNotExist:
                        return Response(
                            data={
                                'code': status.HTTP_200_OK,
                                'status': False,
                                'message': f'Alergia con ID {allergy_id} no encontrada.',
                                'data': None
                            })

            if disabilities:  # Verificar si hay discapacidades para actualizar
                athlete.people.peopledisabilities_set.all().delete()
                for disability_data in disabilities:
                    disability_id = disability_data.get('id')
                    try:
                        disability = Disabilities.objects.get(id=disability_id)
                        peopleDisabilities.objects.create(people=athlete.people, disabilities=disability)
                    except Disabilities.DoesNotExist:
                        return Response(
                            data={
                                'code': status.HTTP_200_OK,
                                'status': False,
                                'message': f'Discapacidad con ID {disability_id} no encontrada.',
                                'data': None
                            })

            if special_conditions:  # Verificar si hay condiciones especiales para actualizar
                athlete.people.peoplespecialconditions_set.all().delete()
                for condition_data in special_conditions:
                    condition_id = condition_data.get('id')
                    try:
                        condition = specialconditions.objects.get(id=condition_id)
                        peoplespecialConditions.objects.create(people=athlete.people, specialconditions=condition)
                    except specialconditions.DoesNotExist:
                        return Response(
                            data={
                                'code': status.HTTP_200_OK,
                                'status': False,
                                'message': f'Condición especial con ID {condition_id} no encontrada.',
                                'data': None
                            })
        
        athlete.save()
        
        serializer = AthleteSerializer(athlete)
        response_data ={
            'code': status.HTTP_200_OK,
            'message': f'Datos de {athlete.people.name} actualizados exitosamente',
            'status': True,
            'data': serializer.data
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
        with transaction.atomic():
            try:
                athlete = Athlete.objects.get(pk=pk)
            except Athlete.DoesNotExist:
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'Atleta no encontrado.',
                    'status': False,
                    'data': None
                }
                return Response(data=response_data)

            athlete_name = athlete.people.name
            
            # Eliminar las relaciones asociadas a la persona del atleta
            athlete.people.peopleallergies_set.all().delete()
            athlete.people.peopledisabilities_set.all().delete()
            athlete.people.peoplespecialconditions_set.all().delete()

            # Eliminar el usuario relacionado
            try:
                user = User.objects.get(people=athlete.people)
                user.delete()
            except User.DoesNotExist:
                pass

            # Finalmente, eliminar al atleta y a la persona del atleta
            athlete.people.delete()
            athlete.delete()

            response_data = {
                'code': status.HTTP_200_OK,
                'message': f'Datos de {athlete_name} eliminados exitosamente',
                'status': True,
                'data': None
            }
            return Response(data=response_data)

    except Exception as e:
        data = {
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
        return Response(data)