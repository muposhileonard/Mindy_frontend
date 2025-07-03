from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.utils import timezone
from datetime import timedelta

class PhoneOTP(models.Model):
    contact = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)

    @staticmethod
    def generate_code():
        return str(random.randint(1000000, 9999999))


class MindyUserManager(BaseUserManager):
    def create_user(self, contact, password=None, **extra_fields):
        if not contact:
            raise ValueError("Contact (email or phone) is required.")
        user = self.model(contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(contact, password, **extra_fields)

class MindyUser(AbstractBaseUser, PermissionsMixin):
    contact = models.CharField(max_length=100, unique=True)
    special_word = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = MindyUserManager()

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = ['special_word']

    def __str__(self):
        return self.contact



