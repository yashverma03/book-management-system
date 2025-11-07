from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'role', 'created_at', 'updated_at', 'deleted_at']
    read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
