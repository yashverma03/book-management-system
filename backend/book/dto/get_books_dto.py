from rest_framework import serializers
import uuid

class GetBooksDto(serializers.Serializer):
  title = serializers.CharField(
    required=False,
    allow_blank=True,
    help_text='Filter by title (case-insensitive partial match)'
  )
  isbn = serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=20,
    help_text='Filter by ISBN (exact match)'
  )
  author = serializers.CharField(
    required=False,
    allow_blank=True,
    help_text='Filter by author (case-insensitive partial match)'
  )
  added_by_user = serializers.UUIDField(
    required=False,
    allow_null=True,
    help_text='Filter by user ID (UUID) who added the book'
  )
