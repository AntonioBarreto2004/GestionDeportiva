from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http.response import HttpResponse
import mimetypes
import os


#Importaciones para el login y logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist

#Formulario de registro
from .forms import RegisterForm
from core.models import Profile, Rol
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import *
from core.models import *



def index(request):
    return render(request,'index.html',{
        #context
    })

#Inicio de sesion
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Buscar el usuario por su correo electrónico
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # El usuario no existe
            messages.error(request, 'Correo no existente')
            return redirect('login')

        # Autenticar al usuario
        authenticated_user = authenticate(username=user.username, password=password)
        if authenticated_user is not None:

            # Iniciar sesión
            login(request, authenticated_user)
            messages.success(request, 'Bienvenido {} {}'.format(authenticated_user.first_name, authenticated_user.last_name))
            return redirect('index')
        else:
            # La contraseña es incorrecta
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('login')

    return render(request, 'users/login.html')


#Cerrar Sesion
def logout_view(request):
    logout(request)
    messages.success(request,'Session finalizada correctamente')
    return redirect('index') 


#Registro de Usuario Persona

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('nombre_persona')
        last_name = request.POST.get('apellido_persona')
        photo_profile = request.FILES.get('Imagen_del_usuario')
        birthdate = request.POST.get('Fecha_de_nacimiento')
        gender = request.POST.get('genero')
        telephone_number = request.POST.get('Telefono')
        allergies = request.POST.get('Alergias')
        disability = request.POST.get('Dicapacidad')
        type_document_id = request.POST.get('tiDocumento')
        if type_document_id:
                type_document_id = int(type_document_id)
        else:
            type_document_id = 0
        type_document = get_object_or_404(DocumentType, id=type_document_id)
        num_document = request.POST.get('num_documento')
        email = request.POST.get('CorreoE')
        password = request.POST.get('password')
        file = request.FILES.get('archivos')
        file_v = request.FILES.get('archivosv')
        file_f = request.FILES.get('archivosf')

        
        try:
            password = str(num_document)  # Convertir el número de documento a cadena
            # Hash de la contraseña
            user = User.objects.create_user(username=email, email=email, password=password)
            user.is_staff = False
            user.is_superuser = False
            group = Group.objects.get(name='Personas_Clientes')
            user.groups.add(group)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            rol = Rol.objects.get(name_rol='Usuario')

            profile = Profile.objects.create(user=user, photo_profile=photo_profile, birthdate=birthdate,
                                                gender=gender, telephone_number=telephone_number, allergies=allergies,
                                                disability=disability, type_document=type_document, num_document=num_document, cod_rol=rol, state=True)

            # Guardar los archivos en el perfil
            profile.file = file
            profile.file_v = file_v
            profile.file_f = file_f
            profile.save()

            if user:
                messages.success(request, 'Registro exitoso (Se ha enviado un mensaje a su correo)')
                return redirect('index')
            
        except:
         messages.error(request, 'Por favor, completa todos los campos del formulario.')

        
     # Pasar los tipos de documentos al contexto de renderizado
    document_types = DocumentType.objects.all()
    return render(request, 'users/register.html', {'document_types': document_types})      
        



def registerIn(request):
    
    if request.method == 'POST':
        username = request.POST.get('nombre_usuario')
        first_name = request.POST.get('nombre_persona')
        last_name = request.POST.get('apellido_persona')
        photo_profile = request.FILES.get('Imagen_del_usuario')
        birthdate = request.POST.get('Fecha_de_nacimiento')
        gender = request.POST.get('genero')
        telephone_number = request.POST.get('Telefono')
        allergies = request.POST.get('Alergias')
        disability = request.POST.get('Dicapacidad')
        state_medic = request.POST.get('estadoMedico')
        vaccines = request.POST.get('vacunasCovid')
        type_document = request.POST.get('tiDocumento')
        num_document = request.POST.get('num_documento')
        email = request.POST.get('CorreoE')
        password = request.POST.get('password')



        

        group = Group.objects.get(name= 'Instructores')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = False
            user.is_superuser = False
            user.groups.add(group)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            rol = Rol.objects.get(name_rol='Instructor')
            
            profile = Profile.objects.create(user=user, photo_profile=photo_profile, birthdate=birthdate, gender=gender,
                                            telephone_number=telephone_number, allergies=allergies, disability=disability, state_medic=state_medic,
                                            vaccines=vaccines, type_document=type_document, num_document=num_document, cod_rol=rol, state=True)
            profile.save()
            

            if user:
            
                messages.success(request, 'Registro exitoso (Sele a enviado un mensaje a su correo)')
                return redirect('index')

         
           
        except:
            messages.error(request, 'Por favor, completa todos los campos del formulario.')

            

    return render(request, 'users/registerI.html', {
    })

#Descarga de Documentos

def descargar_archivo(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    filename = 'Permiso_de_consentimiento_Padres_de_familia_(Menor_de_Edad).pdf'

    filepath = os.path.join(BASE_DIR, 'media', 'media', filename)

    with open(filepath, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mimetypes.guess_type(filepath)[0])
        response['Content-Disposition'] = f"attachment; filename={filename}"

    return response

def descargar_archivo2(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    filename = 'Consentimiento manejo de Datos (Mayores_de_edad).pdf'

    filepath = os.path.join(BASE_DIR, 'media', 'media', filename)

    with open(filepath, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mimetypes.guess_type(filepath)[0])
        response['Content-Disposition'] = f"attachment; filename={filename}"

    return response
