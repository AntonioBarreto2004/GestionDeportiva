from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from . serializer import *

    #DOCUMENTS TYPE
@api_view(['GET']) # METODO GET (LISTAR)
def list_document_types(request):
    queryset = DocumentType.objects.all()
    serializer = DocumentTypeSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_document_type(request):
    serializer = DocumentTypeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_document_type(request, pk):
    try:
        document_type = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = DocumentTypeSerializer(document_type, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_document_type(request, pk):
    try:
        document_type = DocumentType.objects.get(pk=pk)
    except DocumentType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    document_type.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    #ROLE
@api_view(['GET'])
def list_roles(request):
    queryset = Rol.objects.all()
    serializer = RolSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_role(request):
    serializer = RolSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_role(request, pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = RolSerializer(role, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_role(request, pk):
    try:
        role = Rol.objects.get(pk=pk)
    except Rol.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    #PROFILE
@api_view(['GET'])
def list_profiles(request):
    queryset = Profile.objects.all()
    serializer = ProfileSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    profile.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    #USER
@api_view(['GET'])
def list_users(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
