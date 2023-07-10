from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializer import *

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
    
    try:
        serializer.save()
    except ValidationError as e:
        errors = []
        for field, error_list in e.message_dict.items():
            for error in error_list:
                errors.append(f"{field}: {error}")
        
        return Response(data={'code':'400_BAD_REQUEST', 'message': 'Error en la creación del perfil',
                              'errors': errors, 'status': False}, status=status.HTTP_400_BAD_REQUEST)

    # Establecer la foto de perfil si se proporciona en la solicitud
    if 'photo_profile' in request.data:
        photo = request.data['photo_profile']
        profile = serializer.instance
        profile.photo_profile = photo
        profile.save()
    
    return Response(data={'code':'201_CREATED', 'message': 'Usuario creado exitosamente', 'status':True},
                    status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data={'code':'202_ACCEPTED', 'message': 'Usuario Actualizado exitosamente',  'status':True}, status=status.HTTP_202_ACCEPTED)

@api_view(['DELETE'])
def delete_profile(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no exixte',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    profile.delete()
    return Response(data={'code':'204_NO_CONTENT', 'message': 'Usuario eliminado exitosamente',  'status':True}, status=status.HTTP_204_NO_CONTENT)