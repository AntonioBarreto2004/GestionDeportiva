from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializer import *

 #USER
@api_view(['GET'])
def list_users(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

# Envío de correo al crear usuario
def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/email.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = 'SigDep Gestión Deportiva <barreanto20198@gmail.com>'
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_name = serializer.validated_data['name']
    user_email = serializer.validated_data['email']
    user_password = serializer.validated_data['password']
    send_activation_email(user_name,user_email, user_password)
    serializer.save()
    return Response(data={'code':'201_CREATED', 'message': 'Usuario creado exitosamente, se le ha enviado un correo', 'status':True}, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Usuario Actualizado exitosamente',  'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    user.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Usuario eliminado exitosamente',  'status':True}, status=status.HTTP_204_NO_CONTENT)