from django.db import models
from utils.models.enum_field import EnumField
import uuid

class UserRole(models.TextChoices):
  ADMIN = 'admin'
  MANAGER = 'manager'

class User(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
  email = models.EmailField(unique=True)
  name = models.CharField(max_length=255)
  password = models.CharField(max_length=255, null=False)
  role = EnumField(enum_type='users_user_role_enum', default=UserRole.MANAGER, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'users'
    indexes = [
      models.Index(fields=['role']),
    ]

    def __str__(self):
      return f"{self.name} ({self.email})"
