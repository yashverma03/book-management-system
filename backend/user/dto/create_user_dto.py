from rest_framework import serializers
from user.models import UserRole

class CreateUserDto(serializers.Serializer):
  email = serializers.EmailField(
    required=True,
    help_text='User email address'
  )
  name = serializers.CharField(
    required=True,
    help_text='User full name'
  )
  password = serializers.CharField(
    required=True,
    write_only=True,
    min_length=8,
    max_length=128,
    help_text='User password (minimum 8 characters)'
  )
  role = serializers.ChoiceField(
    choices=UserRole.choices,
    required=False,
    help_text='User role - either "admin" or "manager" (defaults to "manager")'
  )
