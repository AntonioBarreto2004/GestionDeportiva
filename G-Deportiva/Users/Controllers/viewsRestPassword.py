import base64
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from g_deprotiva import settings
from django.utils import timezone
from ..models import *
from ..serializers import *

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')

    user = User.objects.filter(email=email).first()
    if not user:
        return Response(
            data={'code':'500_INTERNAL_SERVER_ERROR', 
                  'message': 'Usuario no existe',  
                  'status':False}, 
                  status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    token = default_token_generator.make_token(user)
     # Obtener la marca de tiempo actual
    now = timezone.now()

    # Establecer la fecha y hora de expiración del token (por ejemplo, 1 hora después de la generación)
    token_expiration = now + timezone.timedelta(hours=1)
    uid_base64 = base64.urlsafe_b64encode(force_bytes(user.pk)).decode()

    reset_password_url = f'{settings.RESET_PASSWORD_URL}/{uid_base64}/{token}/'

    subject = 'Restablecer Contraseña'
    message = f'Hola {user.name}, \n \
        Haga clic en el siguiente enlace para restablecer su contraseña: \n \
        {reset_password_url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    return Response(
        data={'code': 'HTTP_200_OK', 
              'message': 'Correo Enviado exitosamente', 
              'status': True}, 
              status=status.HTTP_200_OK
            )




@api_view(['POST'])
def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response(
                data={'code': 'HTTP_400_BAD_REQUEST', 
                      'message': 'Las contraseñas no coinciden', 
                      'status': False}, 
                status=status.HTTP_400_BAD_REQUEST
            )


        user.set_password(new_password)
        user.save()

        subject = 'Contraseña Restablecida Exitosamente'
        message = f'Hola {user.name},\n\nTu contraseña ha sido restablecida exitosamente.\n \
        La nueva contraseña es: {new_password}\n\nSaludos,\nSigDep Gestión Deportiva'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response(
            data={'code':'200_OK', 
                  'message': 'Contraseña restablecida exitosamente', 
                  'status':True}, status=status.HTTP_200_OK
                )

    return Response(
        data={'code':'HTTP_500_INTERNAL_SERVER_ERROR', 
              'message': 'El enlace de restablecimiento de contraseña es inválido', 
              'status':False}, 
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

