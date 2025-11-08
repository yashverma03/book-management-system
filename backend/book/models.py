from django.db import models
from user.models import User

class Book(models.Model):
  id = models.BigAutoField(primary_key=True, null=False)
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  isbn = models.CharField(max_length=20, null=True, blank=True, unique=True)
  added_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, related_name='books')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'books'

    def __str__(self):
      return f"{self.title} ({self.author})"
