from rest_framework import serializers

class UpdateBookDto(serializers.Serializer):
  title = serializers.CharField(
    required=False,
    max_length=255,
    help_text='Book title'
  )
  author = serializers.CharField(
    required=False,
    max_length=255,
    help_text='Book author name'
  )
  description = serializers.CharField(
    required=False,
    allow_blank=True,
    allow_null=True,
    help_text='Book description'
  )
  price = serializers.DecimalField(
    required=False,
    max_digits=10,
    decimal_places=2,
    help_text='Book price'
  )
  isbn = serializers.CharField(
    required=False,
    allow_blank=True,
    allow_null=True,
    max_length=20,
    help_text='International Standard Book Number (ISBN)'
  )
