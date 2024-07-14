from django.db import models
from django.contrib.auth.models import User
from grade.models import Language
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
# Create your models here.


ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)



class Profile(models.Model):
    TYPE_CHOICES = (
    ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='student')
    full_name = models.CharField(max_length=255, null=True, blank=True)    
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username