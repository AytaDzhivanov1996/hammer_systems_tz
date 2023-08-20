from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}

class CustomUserManager(BaseUserManager):
	def create_user(self, phone, password=None):
		if not phone:
			raise ValueError('User must have a phone number')
		if not password:
			raise ValueError('User must have a password')

		user = self.model(phone=phone)
		user.set_password(password)
		user.is_staff=False
		user.is_admin=False
		user.is_active=False
		user.save(using=self._db)
		return user


	def create_superuser(self, phone, password=None):
		user = self.create_user(phone, password=password)
		user.is_staff=True
		user.is_admin=True
		user.save(using=self._db)
		return user
	

class User(AbstractUser):
    objects = CustomUserManager()

    username = None
    phone = PhoneNumberField(unique=True)
    otp = models.CharField(verbose_name='otp', max_length=10, **NULLABLE)
    referral_link = models.CharField(max_length=10, **NULLABLE)
    activated_link = models.CharField(max_length=10, **NULLABLE)
    first_login = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
