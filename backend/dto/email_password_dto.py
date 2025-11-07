from rest_framework import serializers


class EmailPasswordDto(serializers.Serializer):
  email = serializers.EmailField(
    required=True,
    help_text='User email address'
  )
  password = serializers.CharField(
    required=True,
    write_only=True,
    help_text='User password'
  )
