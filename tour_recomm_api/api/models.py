from django.db import models
from rest_framework.response import Response
# Create your models here.

class CustomResponse(Response):
    def __init__(self, status, message, data=None):
        response_data = {'status': status, 'message': message, 'data': data}
        super().__init__(response_data)
    

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    hashpw = models.TextField(null=False, blank=False)
    fullname = models.TextField(null=False, blank=False, max_length = 50)
    dob = models.DateField(null=True, verbose_name="date of birth")
    gender = models.SmallIntegerField(default=0)
    role = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)

    
    