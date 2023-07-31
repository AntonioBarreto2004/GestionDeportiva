import re
import requests
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django_filters import rest_framework as filters
from sigdep.sigdep import settings
from ..models import *
from ..serializers import *


# Envío de correo al crear usuario
def send_activation_email(user_name, user_email, password):
    subject = 'Bienvenido al Sistema SigDep'
    html_message = render_to_string('static/html/correo.html', { 'user_name': user_name,'user_email': user_email, 'password': password})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)


@api_view(['POST'])
def create_user_and_people(request):
    data = request.data

    user_serializer = UserSerializer(data=data.get('user'))
    people_serializer = PeopleSerializer(data=data)

    if user_serializer.is_valid() and people_serializer.is_valid():
        user = user_serializer.save()
        people = people_serializer.save(user=user)
        return Response('Successfully created user and people.')
    else:
        return Response(user_serializer.errors + people_serializer.errors)