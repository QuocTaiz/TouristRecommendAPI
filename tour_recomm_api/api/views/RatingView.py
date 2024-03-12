from rest_framework.views import APIView
from ..models import History, CustomResponse, Tourist, Rating
from ..serializers import RatingSerializer
from ..services import TokenManager, RatingManager
from rest_framework import status

class RatingInfo(APIView):
    http_method_names = ['get', 'head', 'patch']
    
    def get(self, request):
        pass

    def patch(self, request):

        key_token = request.headers.get('Authorization')
        if not TokenManager.verify(key_token):
            return CustomResponse(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED!")

        user_id = TokenManager.getUser(key_token).id

        try:
            obj = Rating.objects.get(user_id = user_id)
        except Rating.DoesNotExist:
            Rating.objects.create(user_id = user_id, tourist_id = request.data['tourist_id'], rate = request.data['rate'])
            return CustomResponse(status.HTTP_205_RESET_CONTENT, "Update rate successful!")
        
        serializer = RatingSerializer(obj, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            RatingManager.update_rating_tourist(request.data['tourist_id'])
        else:
            return CustomResponse(status.HTTP_400_BAD_REQUEST, "Data not valid!")
        return CustomResponse(status.HTTP_205_RESET_CONTENT, "Update rate successful!")

