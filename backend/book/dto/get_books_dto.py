from rest_framework import serializers

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
  added_by_user = serializers.CharField(
    required=False,
    allow_blank=True,
    help_text='Filter by user ID who added the book'
  )
