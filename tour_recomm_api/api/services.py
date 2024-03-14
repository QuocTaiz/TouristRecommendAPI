import hashlib
from .models import Token, User, History, Rating, Tourist
from django.utils.crypto import get_random_string
from django.utils import timezone

class HashPw:
    def hash(pw):
        pw_bytes = pw.encode('utf-8')
        hash_obj = hashlib.sha256(pw_bytes)
        return hash_obj.hexdigest()
    
class TokenManager:

    def random():
        return get_random_string(32)
    
    def getUser(key):
        token = Token.objects.get(key = key)
        user = User.objects.get(id = token.user_id)
        return user
    
    def create(user_id):
        key = TokenManager.random()
        created_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        token = Token.objects.create(user_id = user_id, key = key, created_at = created_at)
        return token
    
    def update(token):
        key = TokenManager.random()
        created_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        token.key = key
        token.created_at = created_at
        token.save()
        return token
    
    def delete(token):
        token.delete()

    def verify(key):
        try:
            token = Token.objects.get(key = key)
            user = User.objects.get(id = token.user_id)
            return user.role
        except Token.DoesNotExist:
            return False

class HistoryWriter:

    def inc_time_visit(user_id, tourist_id):

        last_view = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            htr = History.objects.get(user_id = user_id, tourist_id = tourist_id)
        except History.DoesNotExist:
            History.objects.create(user_id = user_id, tourist_id = tourist_id, last_view = last_view)
        htr = History.objects.get(user_id = user_id, tourist_id = tourist_id)
        htr.time += 1
        htr.last_view = last_view
        htr.save()

class RatingManager:
    def update_rating_tourist(tourist_id):
        list_rate = Rating.objects.raw("select * from api_rating where tourist_id="+str(tourist_id))
        mean = 0
        for rate in list_rate:
            mean += rate.rate
        mean = mean / len(list_rate)

        tourist = Tourist.objects.get(id=tourist_id)
        tourist.rate = round(mean, 1)
        tourist.save()

class Province:

    def getProvince(id):
        
        dict_prv = {1: 'Hà Nội', 2: 'Hải Phòng', 3: 'Đà Nẵng', 4: 'Hồ Chí Minh', 5: 'Cần thơ', 6: 'An Giang', 7: 'Bà Rịa - Vũng Tàu', 8: 'Bắc Giang', 9: 'Bắc Kạn', 10: 'Bạc Liêu', 11: 'Bắc Ninh', 12: 'Bến Tre', 13: 'Bình Định', 14: 'Bình Dương', 15: 'Bình Phước', 16: 'Bình Thuận', 17: 'Cà Mau', 18: 'Cao Bằng', 19: 'Đắk Lắk', 20: 'Đắk Nông', 21: 'Điện Biên', 22: 'Đông Nai', 23: 'Đồng Tháp', 24: 'Gia Lai', 25: 'Hà Giang', 26: 'Hà Nam', 27: 'Hà Tĩnh', 28: 'Hải Dương', 29: 'Hậu Giang', 30: 'Hòa Bình', 31: 'Hưng Yên', 32: 'Khánh Hòa', 33: 'Kiên Giang', 34: 'Kon Tum', 35: 'Lai Châu', 36: 'Lâm Đồng', 37: 'Lạng Sơn', 38: 'Lào Cai', 39: 'Long An', 40: 'Nam Đinh', 41: 'Nghệ An', 42: 'Ninh Bình', 43: 'Ninh Thuận', 44: 'Phú Thọ', 45: 'Phú Yên', 46: 'Quảng Bình', 47: 'Quảng Nam', 48: 'Quảng Ngãi', 49: 'Quảng Ninh', 50: 'Quảng Trị', 51: 'Sóc Trăng', 52: 'Sơn La', 53: 'Tây Ninh', 54: 'Thái Bình', 55: 'Thái Nguyên', 56: 'Thanh Hóa', 57: 'Thừa Thiên Huế', 58: 'Tiền Giang', 59: 'Trà Vinh', 60: 'Tuyên Quang', 61: 'Vĩnh Long', 62: 'Vĩnh Phúc', 63: 'Yên Bái'}

        return dict_prv[int(id)]
    
class TouristSpecial:

    def getSpecial(id):

        dict_spc = {1: 'Du lịch văn hóa', 2: 'Di tích', 3: 'Du lịch tự nhiên', 4: 'Chùa, đình, đền, tháp, nhà thờ, lăng mộ', 5: 'Du lịch thể thao', 6: 'Bảo tàng', 7: 'Du lịch biển', 8: 'Công viên'}

        return dict_spc[int(id)]

