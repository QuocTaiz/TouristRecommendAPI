from rest_framework.views import APIView
from ..models import History, CustomResponse, Tourist
from ..serializers import HistorySerializer, TouristSerializer
from ..services import TokenManager
from rest_framework import status

class HistoryInfo(APIView):
    http_method_names = ['get', 'head']
    
    def get(self, request):

        key_token = request.headers.get('Authorization')

        if not TokenManager.verify(key_token):
            return CustomResponse(status.HTTP_401_UNAUTHORIZED, 'UNAUTHORIZED!')

        user_id = TokenManager.getUser(key_token).id

        try:
            obj = History.objects.raw("select * from api_history where user_id="+str(user_id)+" order by last_view desc")
        except History.DoesNotExist:
            return CustomResponse(status.HTTP_404_NOT_FOUND, "Not found history!")
        

        serializer = HistorySerializer(obj, many=True)
        for ser_data in serializer.data:
            ser_data['tourist'] = TouristSerializer(Tourist.objects.get(id = ser_data['tourist_id'])).data

        return CustomResponse(status.HTTP_200_OK, 'OK', serializer.data)

