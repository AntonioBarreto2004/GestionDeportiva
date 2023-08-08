from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from rest_framework import status


@api_view(['PATCH'])
def update_profile_photo(request, people_id):
    try:
        people = People.objects.get(id=people_id)
        new_photo = request.data.get('photo_user')
        if not People:
            return Response(data={'code': status.HTTP_200_OK, 
                                  'message': 'Usuario no existe',  
                                  'status':False ,
                                  'data': None})

        if not People.photo_user:
            people.photo_user = new_photo
        else:
            people.photo_user.delete() 
            people.photo_user = new_photo 

        people.save()

        return Response(data={'code': status.HTTP_200_OK, 
                              'message': 'Foto de perfil actualizada correctamente', 
                              'status':True, 
                              'data':None})

    except People.DoesNotExist:
        return Response(data={'code':status.HTTP_200_OK, 
                              'message': 'Usuario no existe',  
                              'status':False, 'data': None})

    except Exception as e:
        return Response(data={'message': str(e)}, )

