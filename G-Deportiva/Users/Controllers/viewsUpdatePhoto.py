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
            return Response(data={'code': status.HTTP_200_OK, 'message': 'Usuario no existe',  'status':False ,'data': None}, )

        if not user.photo_profile:
            user.photo_profile = new_photo
        else:
            user.photo_profile.delete() 
            user.photo_profile = new_photo 

        user.save()

        return Response(data={'code': status.HTTP_200_OK, 'message': 'Foto de perfil actualizada correctamente', 'status':True, 'data':None}, )

    except User.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 'message': 'Usuario no existe',  'status':False, 'data': None}, )

    except Exception as e:
        return Response(data={'message': str(e)}, )

