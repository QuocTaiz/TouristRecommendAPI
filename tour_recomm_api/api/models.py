from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    hashpw = models.TextField(null=False, blank=False)
    fullname = models.TextField(null=False, blank=False, max_length = 50)
    dob = models.DateField(null=True, verbose_name="date of birth")
    gender = models.SmallIntegerField(default=0)
    role = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False)

    
    