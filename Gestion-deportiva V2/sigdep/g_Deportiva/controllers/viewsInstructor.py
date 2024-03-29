import re
from django.conf import settings
from django.db import transaction
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_instructors(request):
    instructors = Instructors.objects.all().order_by('id')

    instructor_data = []
    for instructor in instructors:
        try:
            user = User.objects.get(people=instructor.people)
            rol_name = user.rol.name if user and user.rol else None
        except User.DoesNotExist:
            rol_name = None

        allergies_data = []
        disabilities_data = []
        special_conditions_data = []

        if instructor.people.peopleallergies_set.exists():
            allergies_data = [
                {
                    'id': allergy.allergies.id,
                    'allergie_name': allergy.allergies.name,
                    'description': allergy.allergies.description
                }
                for allergy in instructor.people.peopleallergies_set.all()
            ]

        if instructor.people.peopledisabilities_set.exists():
            disabilities_data = [
                {
                    'id': disability.disabilities.id,
                    'disability_name': disability.disabilities.name,
                    'description': disability.disabilities.description
                }
                for disability in instructor.people.peopledisabilities_set.all()
            ]

        if instructor.people.peoplespecialconditions_set.exists():
            special_conditions_data = [
                {
                    'id': condition.specialconditions.id,
                    'name': condition.specialconditions.name,
                    'description': condition.specialconditions.description
                }
                for condition in instructor.people.peoplespecialconditions_set.all()
            ]

        birthdate = instructor.people.birthdate
        age = relativedelta(datetime.now().date(), birthdate).years

        instructor_info = {
            'id': instructor.id,
            'name': f"{instructor.people.name} {instructor.people.last_name}",
            'rol': rol_name,
            'email': instructor.people.email,
            'photo_user': instructor.people.photo_user,
            'age': age,
            'gender': instructor.people.gender,
            'telephone_number': instructor.people.telephone_number,
            'type_document': instructor.people.type_document,
            'num_document': instructor.people.num_document,
            'specialization': instructor.specialization,
            'experience_years': instructor.experience_years,
            'file_documentidentity': instructor.people.file_documentidentity,
            'file_eps_certificate': instructor.people.file_eps_certificate,
            'file_informed_consent': instructor.people.file_informed_consent,
            'allergies': allergies_data,
            'disabilities': disabilities_data,
            'special_conditions': special_conditions_data,
            'modified_at': instructor.people.modified_at,
        }
        instructor_data.append(instructor_info)

    if not instructor_data:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'No se encuentran Datos',
            'data': None
        }
    else:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': True,
            'message': 'Consulta realizada exitosamente',
            'data': instructor_data
        }

    return Response(response_data)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$')
# Envío de correo al crear usuario
def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/correo.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)

@api_view(['POST'])
def create_instructor(request):
    try:
        with transaction.atomic():
            # Obtener los datos del cuerpo de la solicitud
            person_data = request.data.get('people')
            specialization = person_data.get('specialization')
            experience_years = person_data.get('experience_years')
            email = person_data['email']

            # Validar que specialization y experience_years no estén vacíos y experience_years sea un valor numérico
            if not specialization or (not experience_years or not experience_years.isdigit()):
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'status': True,
                        'message': 'Los campos "specialization" y "experience_years" deben ser no vacíos y "experience_years" debe ser un valor numérico.',
                        'data': None
                    })
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
            
            # Validate email format
            if not EMAIL_REGEX.match(email):
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'status': True,
                        'message': 'El formato del correo electrónico es inválido.',
                        'data': None
                    })
            # Verificar si ya existe un usuario con esta dirección de correo electrónico
            if People.objects.filter(email=email).exists():
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'message': 'Ya existe un usuario con este correo registrado',
                        'status': True,
                        'data': None
                    })
            num_document = person_data['num_document']

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

            if not re.match(r'^[a-zA-Z\s]+$', name) or not re.match(r'^[a-zA-Z\s]+$', last_name):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'El nombre y apellido del usuario solo pueden contener letras y espacios.',
                    'status': True
                }
                return Response(response_data)
            
            if not re.match(r'^[a-zA-Z\s]+$', type_document):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message': 'El Tipo de documento solo pueden contener letras y espacios.',
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
            
            phone_number = person_data['telephone_number']

            if not re.match(r'^\d{10}$', phone_number):
                response_data = {
                    'code': status.HTTP_200_OK,
                    'message':'El numero telefonico solo puede contener 10 Digitos y Ninguna letra',
                    'status': True
                }
                return Response(response_data)

            # Crear la instancia de People
            people_serializer = PeopleSerializer(data=person_data)
            if people_serializer.is_valid():
                person = people_serializer.save()
            else:
                person.delete()
                return Response(people_serializer.errors)

            # Verificar si ya existe un instructor con la misma persona asociada
            if Instructors.objects.filter(people=person).exists():
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'status': True,
                        'message': 'Ya existe un instructor asociado a esta persona.',
                        'data': None
                    })
            # Crear el instructor
            instructor = Instructors.objects.create(
                people=person,
                specialization=person_data.get('specialization'),
                experience_years=person_data.get('experience_years')
            )

            # Buscar el rol "Instructor" en la base de datos y asignarlo al usuario
            try:
                instructor_role = Rol.objects.get(name='Instructor')
            except Rol.DoesNotExist:
                return Response(
                    data={
                        'code': status.HTTP_200_OK,
                        'status': True,
                        'message': 'El rol "Instructor" no existe.',
                        'data': None
                    })

            # Obtener el número de documento y convertirlo en cadena
            str(person_data.get('num_document'))
            generated_password = str(num_document)  # Generar contraseña basada en el número de documento

            # Crear el usuario y asignar el rol de Instructor
            User.objects.create(
                people=person,
                rol=instructor_role,
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
                    peoplespecialConditions.objects.create(people=person, specialConditions=condition)

                instructor_serializer = InstructorSerializer(instructor)

                 # Envío del correo electrónico
                send_activation_email(person.name, person.email, generated_password)
            # Devolver la respuesta exitosa
            return Response(
                data={
                    'code': status.HTTP_201_CREATED,
                    'status': True,
                    'message': 'Registro realizado con éxito.',
                    'data': instructor_serializer.data
                })
    except User.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'status': True,
                'message': 'El usuario no existe.',
                'data': None
            })



@api_view(['PATCH'])
def update_instructor(request, pk):
    try:
        # Obtener el instructor por su ID
        instructor = Instructors.objects.get(pk=pk)

        people_data = request.data.get('people', {})
        allergies = request.data.get('allergies', [])
        disabilities = request.data.get('disabilities', [])
        special_conditions = request.data.get('special_conditions', [])

        # Actualizar datos de People
        if people_data:
            if 'name' in people_data:
                name = people_data['name']
                if not re.match(r'^[a-zA-Z\s]+$', name):
                    response_data = {
                        'code': status.HTTP_200_OK,
                        'message': 'Nombre de la persona solo puede contener letras y espacios.',
                        'status': False
                    }
                    return Response(response_data)
                instructor.people.name = name

            if 'last_name' in people_data:
                last_name = people_data['last_name']
                if not re.match(r'^[a-zA-Z\s]+$', last_name):
                    response_data = {
                        'code': status.HTTP_200_OK,
                        'message': 'Apellido de la persona solo puede contener letras y espacios.',
                        'status': False
                    }
                    return Response(response_data)
                instructor.people.last_name = last_name

            # ... actualizar otros campos de People ...

            instructor.people.save()  # Guardar cambios en People

        # Manejar campos de archivo si se proporcionan en la solicitud
        if 'photo_user' in request.FILES:
            instructor.people.photo_user = request.FILES['photo_user']
        else:
            instructor.people.photo_user = None
        if 'file_documentidentity' in request.FILES:
            instructor.people.file_documentidentity = request.FILES['file_documentidentity']
        else:
            instructor.people.file_documentidentity = None
        if 'file_EPS_certificate' in request.FILES:
            instructor.people.file_eps_certificate = request.FILES['file_eps_certificate']
        else:
            instructor.people.file_eps_certificate = None
        if 'file_informed_consent' in request.FILES:
            instructor.people.file_informed_consent = request.FILES['file_informed_consent']
        else:
            instructor.people.file_informed_consent = None
        # ... manejar otros campos de archivo ...

        # Guardar cambios en People
        instructor.people.save()

        # Obtener los datos a actualizar del cuerpo de la solicitud
        specialization = request.data.get('specialization')
        experience_years = request.data.get('experience_years')

        # Actualizar los campos si se proporcionaron en la solicitud
        if specialization:
            instructor.specialization = specialization
        if experience_years:
            instructor.experience_years = experience_years

        # Resto del código para manejar las relaciones muchos a muchos
        

        with transaction.atomic():
            if allergies:  # Verificar si hay alergias para actualizar
                instructor.people.peopleallergies_set.all().delete()
                for allergy_data in allergies:
                    allergy_id = allergy_data.get('id')
                    try:
                        allergy = Allergies.objects.get(id=allergy_id)
                        peopleallergies.objects.create(people=instructor.people, allergies=allergy)
                    except Allergies.DoesNotExist:
                        return Response(
                            data={
                                'code': status.HTTP_200_OK,
                                'status': False,
                                'message': f'Alergia con ID {allergy_id} no encontrada.',
                                'data': None
                            })

            if disabilities:  # Verificar si hay discapacidades para actualizar
                instructor.people.peopledisabilities_set.all().delete()
                for disability_data in disabilities:
                    disability_id = disability_data.get('id')
                    try:
                        disability = Disabilities.objects.get(id=disability_id)
                        peopleDisabilities.objects.create(people=instructor.people, disabilities=disability)
                    except Disabilities.DoesNotExist:
                        return Response(
                            data={
                                'code': status.HTTP_200_OK,
                                'status': False,
                                'message': f'Discapacidad con ID {disability_id} no encontrada.',
                                'data': None
                            })

            if special_conditions:  # Verificar si hay condiciones especiales para actualizar
                instructor.people.peoplespecialconditions_set.all().delete()
                for condition_data in special_conditions:
                    condition_id = condition_data.get('id')
                    try:
                        condition = specialconditions.objects.get(id=condition_id)
                        peoplespecialConditions.objects.create(people=instructor.people, specialconditions=condition)
                    except specialconditions.DoesNotExist:
                        return Response(
                            data={
                                'code': status.HTTP_200_OK,
                                'status': False,
                                'message': f'Condición especial con ID {condition_id} no encontrada.',
                                'data': None
                            })

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
                'status': True,
                'message': 'El instructor no existe.',
                'data': None
            })


    

@api_view(['DELETE'])
def delete_instructor(request, pk):
    try:
        # Obtener el instructor
        instructor = Instructors.objects.get(pk=pk)

        with transaction.atomic():
            # Eliminar las relaciones asociadas a la persona del instructor
            instructor.people.peopleallergies_set.all().delete()
            instructor.people.peopledisabilities_set.all().delete()
            instructor.people.peoplespecialconditions_set.all().delete()

            # Eliminar el usuario relacionado
            try:
                user = User.objects.get(people=instructor.people)
                user.delete()
            except User.DoesNotExist:
                pass

            # Finalmente, eliminar al instructor y a la persona del instructor
            instructor.people.delete()
            instructor.delete()

        # Devolver la respuesta
        return Response(
            data={
                'code': status.HTTP_200_OK, 
                'status': True, 
                'message': 'Instructor eliminado exitosamente',
            }
        )

    except Instructors.DoesNotExist:
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'Instructor no existente',
            'status': True,
            'data': None
        }
        return Response(response_data)

