from django.db import models
from rest_framework.response import Response
from django.core.validators import MinValueValidator, MaxValueValidator
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

class Tourist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False, blank=False)
    special = models.TextField(null=False, blank=False)
    area = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    info = models.TextField(null=False, blank=False)
    url_imgs = models.TextField(null=False, blank=False)
    time_visit = models.IntegerField(default=0)
    rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]    
    )

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False, blank=False)
    tourist_id = models.IntegerField(null=False, blank=False)
    time = models.IntegerField(default=0)
    last_view = models.DateTimeField(null=False, blank=False)

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False, blank=False)
    tourist_id = models.IntegerField(null=False, blank=False)
    rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]    
    )

class Token(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False, blank=False, unique=True)
    key = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)
    