from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from rest_framework import status


@api_view(['PATCH'])
def update_profile_photo(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        new_photo = request.data.get('photo_profile')
        if not user:
            return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no existe',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not user.photo_profile:
            user.photo_profile = new_photo
        else:
            user.photo_profile.delete() 
            user.photo_profile = new_photo 

        user.save()

        return Response(data={'code':'HTTP_200_OK', 'message': 'Foto de perfil actualizada correctamente', 'status':True}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={'code':'500_INTERNAL_SERVER_ERROR', 'message': 'Usuario no existe',  'status':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

