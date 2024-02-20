import hashlib

class HashPw:
    def hash(pw):
        pw_bytes = pw.encode('utf-8')
        hash_obj = hashlib.sha256(pw_bytes)
        return hash_obj.hexdigest()
    
# 1