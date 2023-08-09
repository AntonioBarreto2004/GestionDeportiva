import re
from django.conf import settings
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


from ..models import *
from ..serializers import *

@api_view(['GET'])
def list_users(request):
        # Obtener los parámetros de consulta
        email = request.query_params.get('email')
        name = request.query_params.get('name')
        last_name = request.query_params.get('last_name')
        birthdate = request.query_params.get('birthdate')
        gender = request.query_params.get('gender')
        date_create = request.query_params.get('date_create')
        type_document_id = request.query_params.get('type_document_id')
        num_document = request.query_params.get('num_document')
        rol = request.query_params.get('rol')
        # Crear un diccionario con los parámetros de consulta que se proporcionaron
        filters = {}
        if email:
            filters['email__icontains'] = email
        if name:
            filters['name__icontains'] = name
        if last_name:
            filters['last_name__icontains'] = last_name
        if birthdate:
            filters['birthdate'] = birthdate
        if gender:
            filters['gender__icontains'] = gender
        if date_create:
            filters['date_create'] = date_create
        if type_document_id:
            filters['type_document_id__icontains'] = type_document_id
        if num_document:
            filters['num_document'] = num_document
        if rol:
            filters['users__rol__name_rol__icontains'] = rol
        # Obtener todos los objetos People que coincidan con los parámetros de consulta
        people = People.objects.filter(**filters)
        # Comprobar si hay datos
        if not people:
            return Response(
                data={
                    'code': status.HTTP_200_OK, 
                    'status': False, 
                    'message': 'No hay datos disponibles',
                    'data': None
                })
        # Serializar los objetos People y obtener los usuarios y nombres de rol asociados
        people_data = []
        for person in people:
            person_data = PeopleSerializer(person).data
            user = User.objects.get(people=person)
            user_data = UserSerializer(user).data
            person_data['users'] = user_data
            rol_name = Rol.objects.get(id=user_data['rol']).name_rol if 'rol' in user_data else None
            person_data['users']['rol_name'] = rol_name

            # Obtener alergias asociadas
            allergies = person.peopleallergies_set.all()
            allergy_data = [AllergiesSerializer(allergy.allergies).data for allergy in allergies]
            person_data['allergies'] = allergy_data

            # Obtener discapacidades asociadas
            disabilities = person.peopledisabilities_set.all()
            disability_data = [DisabilitiesSerializer(disability.disabilities).data for disability in disabilities]
            person_data['disabilities'] = disability_data

            # Obtener condiciones especiales asociadas
            special_conditions = person.peoplespecialconditions_set.all()
            special_conditions_data = [specialConditionsSerializer(condition.specialConditions).data for condition in special_conditions]
            person_data['special_conditions'] = special_conditions_data

            people_data.append(person_data)

        # Devolver la respuesta con la lista de personas y usuarios asociados
        return Response(
            data={
                'code': status.HTTP_200_OK, 
                'status': True, 
                'message': 'Listado de usuarios y personas obtenido exitosamente',
                'data': {'people': people_data}
                })
    
# Envío de correo al crear usuario
def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/correo.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)


@api_view(['POST'])
def create_user(request):
    data = request.data

    people_data = data.get('people')
    user_data = data.get('user')

    # Validar que los campos requeridos no estén vacíos
    empty_fields = []
    required_fields = ['email', 'name', 'last_name', 'num_document', 'birthdate', 
                       'telephone_number', 'type_document_id', 'gender']
    for field in required_fields:
        if not people_data.get(field):
            empty_fields.append(field)

    if empty_fields:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'Los siguientes campos no pueden estar vacíos',
                'status': False,
                'data': f'{empty_fields}'
            })
    # Realizar verificación adicional para evitar usuarios duplicados
    email = people_data['email']
    num_document = people_data['num_document']

    if People.objects.filter(email=email).exists():
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'Ya existe un usuario con este correo registrado',
                'status': False,
                'data': None
            })

    if People.objects.filter(num_document=num_document).exists():
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'Ya existe un usuario con este número de documento',
                'status': False,
                'data': None
            })

    # Validar nombre y apellido
    name = people_data['name']
    last_name = people_data['last_name']

    if not re.match(r'^[a-zA-Z\s]+$', name) or not re.match(r'^[a-zA-Z\s]+$', last_name):
        response_data = {
            'code': status.HTTP_200_OK,
            'message': 'El nombre y apellido del usuario solo pueden contener letras y espacios.',
            'status': False
        }
        return Response(response_data)

    # Validar el número de documento
    if not re.fullmatch(r'^\d{8,10}$', str(num_document)):
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'El número de documento debe tener entre 8 y 10 dígitos.',
            'data': None
        }
        return Response(response_data)

    # Validar la contraseña
    password = user_data.get('password')  # Asegúrate de que 'password' es una clave en tu diccionario de datos

    # Si no se proporciona una contraseña, envía un error.
    if not password:
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'No se proporcionó una contraseña.',
            'data': None
        }
        return Response(response_data)

    if not re.fullmatch(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.{12,}).*$', password):
        response_data = {
            'code': status.HTTP_200_OK,
            'status': False,
            'message': 'La contraseña debe tener más de 12 caracteres, contener al menos una letra mayúscula, una letra minúscula y un número.',
            'data': None
        }
        return Response(response_data)

    # Crear la instancia de People
    people_serializer = PeopleSerializer(data=people_data)
    if people_serializer.is_valid():
        people = people_serializer.save()
    else:
        return Response(people_serializer.errors)

    # Manejar las relaciones muchos a muchos
    if 'allergies' in people_data:
        allergies_ids = people_data['allergies']
        allergies_associated = Allergies.objects.filter(id__in=allergies_ids)
        for allergy in allergies_associated:
            peopleAllergies.objects.create(people=people, allergies=allergy)

    if 'disabilities' in people_data:
        disabilities_ids = people_data['disabilities']
        disabilities_associated = Disabilities.objects.filter(id__in=disabilities_ids)
        for disability in disabilities_associated:
            peopleDisabilities.objects.create(people=people, disabilities=disability)

    if 'special_conditions' in people_data:
        special_conditions_ids = people_data['special_conditions']
        special_conditions_associated = specialConditions.objects.filter(id__in=special_conditions_ids)
        for condition in special_conditions_associated:
            peoplespecialConditions.objects.create(people=people, specialConditions=condition)

    # Paso 2: Crear la instancia de User y asociarlo con People
    if user_data:
        user = User()
        user.people = people
        user.rol_id = user_data['rol']
        user.is_active = True  # Establecer el usuario como activo
        user.set_password(user_data['password'])  # Establecer la contraseña utilizando set_password()
        user.save()

        # Paso 3: Enviar el correo de activación
        send_activation_email(people.name, people.email, user_data['password'])

    # Paso 4: Devolver la respuesta
    response_data = {
        'code': status.HTTP_201_CREATED,
        'status': True,
        'message': 'Usuario creado exitosamente, se le ha enviado un correo.',
        'data': None
    }
    return Response(response_data, status=status.HTTP_201_CREATED)

    

@api_view(['PATCH'])
def update_user(request, pk):
    try:
        people = People.objects.get(pk=pk)

        people_data = request.data.get('people')
        if people_data:
            serializerPd = PeopleSerializer(people, data=people_data, partial=True)
            serializerPd.is_valid(raise_exception=True)
            people = serializerPd.save()  # Actualiza los datos de People

        if 'photo_user' in request.FILES:
            people.photo_user = request.FILES['photo_user']

        name = request.data.get('name')  # Obtén el nombre de los datos de la solicitud
        last_name = request.data.get('last_name')  # Obtén el apellido de los datos de la solicitud

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

        # Nuevas validaciones
        non_updateable_fields = ['birthdate', 'num_document']
        for field in non_updateable_fields:
            if field in request.data:
                return Response(
                    data={'code': status.HTTP_200_OK,
                          'message': f'No se puede actualizar el campo: {field}',
                          'status': False,
                          'data': None
                          },
                )
        num_telefono = request.data.get('num_telefono')
        if num_telefono and not re.fullmatch(r'^\d{10}$', num_telefono):
            return Response(
                data={'code': status.HTTP_200_OK,
                      'message': 'El número de teléfono debe tener exactamente 10 dígitos.',
                      'status': False,
                      'data': None
                      },
            )

        # Actualizar los datos de User (si existen en la solicitud)
        user_data = request.data.get('user')
        if user_data:
            user = User.objects.get(people=people)
            user.rol_id = user_data.get('rol', user.rol_id)
            user.save()

        # Actualizar alergias, discapacidades y condiciones especiales
        allergies = request.data.get('allergies', [])
        disabilities = request.data.get('disabilities', [])
        special_conditions = request.data.get('special_conditions', [])

        # Eliminar registros existentes
        people.peopleallergies_set.all().delete()
        people.peopledisabilities_set.all().delete()
        people.peoplespecialconditions_set.all().delete()

        # Crear nuevos registros
        for allergy_id in allergies:
            allergy = Allergies.objects.get(id=allergy_id)
            peopleAllergies.objects.create(people=people, allergies=allergy)

        for disability_id in disabilities:
            disability = Disabilities.objects.get(id=disability_id)
            peopleDisabilities.objects.create(people=people, disabilities=disability)

        for condition_id in special_conditions:
            condition = specialConditions.objects.get(id=condition_id)
            peoplespecialConditions.objects.create(people=people, specialConditions=condition)

        # Actualizar el campo modified_at con la fecha y hora actual
        people.modified_at = timezone.localtime()
        people.save()

        return Response(
            data={'code': status.HTTP_202_ACCEPTED,
                  'message': 'Datos actualizados exitosamente',
                  'status': True,
                  'data': people.modified_at},
        )

    except People.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK,
                  'message': 'Persona no existe',
                  'status': False,
                  'data': None
                  },
        )

    except Allergies.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK,
                  'message': 'Una o más alergias especificadas no existen',
                  'status': False,
                  'data': None
                  },
        )

    except Disabilities.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK,
                  'message': 'Una o más discapacidades especificadas no existen',
                  'status': False,
                  'data': None
                  },
        )

    except specialConditions.DoesNotExist:
        return Response(
            data={'code': status.HTTP_200_OK,
                  'message': 'Una o más condiciones especiales especificadas no existen',
                  'status': False,
                  'data': None
                  },
        )

    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'status': False,
            'message': 'Error del servidor',
            'data': None
        }
        return Response(data)


@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        # Buscar la persona por su ID
        people = People.objects.get(pk=pk)
    except People.DoesNotExist:
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': 'La persona no existe',
                'status': False,
                'data': None
            },
            status=status.HTTP_200_OK
        )

    # Si la persona existe, intentamos eliminar al usuario relacionado si existe
    try:
        user = User.objects.get(pk=pk)
        user.delete()
    except User.DoesNotExist:
        pass

    # Finalmente, eliminamos la persona
    people.delete()

    return Response(
        data={
            'code': status.HTTP_200_OK,
            'message': 'Usuario eliminado exitosamente',
            'status': True,
            'data': None
        },
        status=status.HTTP_200_OK
    )

