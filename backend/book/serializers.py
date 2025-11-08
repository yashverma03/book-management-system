from rest_framework import serializers
from book.models import Book
from user.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
  added_by = UserSerializer(read_only=True)

  class Meta:
    model = Book
    fields = '__all__'
