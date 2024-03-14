from rest_framework.views import APIView
from ..models import CustomResponse, Rating, Tourist, History
from ..serializers import TouristSerializer
from ..services import TokenManager
from rest_framework import status
from ..recommender import Recommander

class RecommanderInfo(APIView):
    http_method_names = ['get', 'head']
    
    df = Recommander.get_final_data()

    def get(self, request):

        key_token = request.headers.get('Authorization')
        if not TokenManager.verify(key_token):
            return CustomResponse(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED!")

        user_id = TokenManager.getUser(key_token).id

        limit = request.query_params.get('limit')
        history_tourist_id = History.objects.filter(user_id=user_id).latest('last_view').tourist_id
        tourist_name = Tourist.objects.get(id=history_tourist_id).name
        df_recommand = None
        if limit == None:
            df_recommand = Recommander.get_recommend(self.df, tourist_name)
        else:
            df_recommand = Recommander.get_recommend(self.df, tourist_name, int(limit))

        list_recommend_tourist = []
        for index in df_recommand.index:
            tourist = Tourist.objects.get(name = df_recommand['Neighbourhood'][index])
            list_recommend_tourist.append(tourist)
        serializer = TouristSerializer(list_recommend_tourist, many=True)
        return CustomResponse(status.HTTP_200_OK, "Get recommend tourist successful!", serializer.data)


