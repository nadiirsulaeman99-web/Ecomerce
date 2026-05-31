from calendar import day_name

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import pycountry


class Create_acount(BaseUserManager):
    def create_user(self,username, first_name, last_name, email, country, password=None, **extra_fields):
        if not email:
            raise ValueError('User most have an email addrsse...')
        if not username:
            raise ValueError('User most have an Username...')
        
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            country = country,
            email = self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None,  **extra_fields):
        
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superadmin', True)
        
        
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password=password,
            first_name=extra_fields.pop('first_name'),
            last_name=extra_fields.pop('last_name'),
            country=extra_fields.pop('country','US'),
            **extra_fields,
        )
        return user
    

class Acount(AbstractBaseUser):
    
    @staticmethod
    def get_country():
        countries = list(pycountry.countries)
        country_choices = [(country.alpha_2, country.name) for country in countries]
        return country_choices
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, )
    country = models.CharField(max_length=2, choices=get_country())

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    is_active     = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_admin      = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country']

    objects = Create_acount()


    def __str__(self):
        return self.username
    

    def is_superuser(self):
        return self.is_admin


    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username or self.email.split('@')[0]
