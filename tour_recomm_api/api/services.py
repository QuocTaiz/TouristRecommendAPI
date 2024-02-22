import hashlib
from .models import Token, User
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

