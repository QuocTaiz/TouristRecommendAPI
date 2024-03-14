from rest_framework.views import APIView
from ..models import Tourist, CustomResponse
from ..services import Province, TouristSpecial, TokenManager, HistoryWriter
from ..serializers import TouristSerializer
from rest_framework import status

class TouristDetail(APIView):
    http_method_names = ['get', 'head']

    def get(self, request):

        limit = 0
        if not request.query_params.get('limit') == None:
            limit = request.query_params.get('limit')

        area_id = 0
        if not request.query_params.get('area_id') == None:
            area_id = request.query_params.get('area_id')

        special_id = 0
        if not request.query_params.get('special_id') == None:
            special_id = request.query_params.get('special_id')

        sql_query = "select * from api_tourist where 1"
        
        if area_id != 0:
            area = Province.getProvince(area_id)
            sql_query += " and area= '" + area + "'"
        
        if special_id != 0:
            special = TouristSpecial.getSpecial(special_id)
            sql_query += " and special= '" + special + "'"

        if limit != 0:
            sql_query += " limit " + limit; 
        
        list_tourist = Tourist.objects.raw(sql_query)

        serializer = TouristSerializer(list_tourist, many=True)

        return CustomResponse(status.HTTP_200_OK, 'OK', serializer.data)

class TouristInfo(APIView):
    http_method_names = ['get', 'head']
    
    def get(self, request, id):

        try:
            tourist = Tourist.objects.get(id=id)
        except Tourist.DoesNotExist:
            return CustomResponse(status.HTTP_404_NOT_FOUND, "Not found tourist!")
        
        key_token = request.headers.get('Authorization')

        if TokenManager.verify(key_token):
            user_id = TokenManager.getUser(key_token).id
            HistoryWriter.inc_time_visit(user_id, id)

        tourist.time_visit += 1
        tourist.save()

        serializer = TouristSerializer(tourist)

        return CustomResponse(status.HTTP_200_OK, 'OK', serializer.data)

class TouristRecommend(APIView):
    http_method_names = ['get', 'head']

    # def get(self, request):
