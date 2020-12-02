import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

GENDER = (
  ("MALE", "MALE"),
  ("FEMALE", "FEMALE")
)

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  fullname = models.CharField(max_length=100, blank=True, null=True)
  phone_number = models.CharField(max_length=100, unique=True, db_index=True)
  password = models.CharField(max_length=255, default='password')
  gender = models.CharField(max_length=10, choices=GENDER, blank=True, null=True)
  date_of_birth = models.DateField(blank=True, null=True)
  lga = models.CharField(max_length=200, blank=True, null=True)
  town = models.CharField(max_length=200, blank=True, null=True)
  preferred_pharmacy = models.CharField(max_length=200, blank=True, null=True)
  preferred_hospital = models.CharField(max_length=200, blank=True, null=True)
  preferred_laboratory = models.CharField(max_length=200, blank=True, null=True)
  date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  verified = models.BooleanField(default=False)
  updated_at = models.DateTimeField(auto_now=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'phone_number'
  REQUIRED_FIELDS = []

  class Meta:
    ordering = ('date_joined',)

  def __str__(self):
    return self.phone_number
